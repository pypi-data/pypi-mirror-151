# This file attempts to do a direct port of CPython binascii code for comparison and testing purposes.
# It may help some Python programmers with little C experience see how this stuff works.
# Obviously, we're going to be trimming out all the CPython generated code and interfacing to leave something pure.

from email.policy import strict
from io import BytesIO
from string import ascii_lowercase
import string
from typing import List, Optional

class Error(Exception):
    pass

BASE64_PAD: bytes = b'='

# n: Faster than using lookups, painful to look at.
TABLE_A2B_BASE64: List[int] = [
    -1, -1, -1, -1,  -1, -1, -1, -1,  -1, -1, -1, -1,  -1, -1, -1, -1,
    -1, -1, -1, -1,  -1, -1, -1, -1,  -1, -1, -1, -1,  -1, -1, -1, -1,
    -1, -1, -1, -1,  -1, -1, -1, -1,  -1, -1, -1, 62,  -1, -1, -1, 63,
    52, 53, 54, 55,  56, 57, 58, 59,  60, 61, -1, -1,  -1,  0, -1, -1, # Note PAD->0
    -1,  0,  1,  2,   3,  4,  5,  6,   7,  8,  9, 10,  11, 12, 13, 14,
    15, 16, 17, 18,  19, 20, 21, 22,  23, 24, 25, -1,  -1, -1, -1, -1,
    -1, 26, 27, 28,  29, 30, 31, 32,  33, 34, 35, 36,  37, 38, 39, 40,
    41, 42, 43, 44,  45, 46, 47, 48,  49, 50, 51, -1,  -1, -1, -1, -1,

    -1, -1, -1, -1,  -1, -1, -1, -1,  -1, -1, -1, -1,  -1, -1, -1, -1,
    -1, -1, -1, -1,  -1, -1, -1, -1,  -1, -1, -1, -1,  -1, -1, -1, -1,
    -1, -1, -1, -1,  -1, -1, -1, -1,  -1, -1, -1, -1,  -1, -1, -1, -1,
    -1, -1, -1, -1,  -1, -1, -1, -1,  -1, -1, -1, -1,  -1, -1, -1, -1,
    -1, -1, -1, -1,  -1, -1, -1, -1,  -1, -1, -1, -1,  -1, -1, -1, -1,
    -1, -1, -1, -1,  -1, -1, -1, -1,  -1, -1, -1, -1,  -1, -1, -1, -1,
    -1, -1, -1, -1,  -1, -1, -1, -1,  -1, -1, -1, -1,  -1, -1, -1, -1,
    -1, -1, -1, -1,  -1, -1, -1, -1,  -1, -1, -1, -1,  -1, -1, -1, -1,
]
TABLE_B2A_BASE64: bytes = b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'

def binascii_a2b_base64_impl(data: bytes, strict_mode: bool = False) -> Optional[bytes]:
    ascii_data: bytes = data
    ascii_len: int = len(data)
    padding_started: int = 0

    # Allocate the buffer
    bin_len: int = ((ascii_len+3)/4)*3 # Upper bound, corrected later
    #writer: BytesIO = BytesIO() - n: I don't think this is used other than for initializing bin_data.
    bin_data = bytes(bin_len)
    if bin_data is None:
        return None
    
    if strict_mode and ascii_len > 0 and ascii_data[0] == '=':
        raise Error('Loading padding not allowed')
    
    quad_pos: int = 0
    leftchar: int = 0
    pads: int = 0
    bdpos: int = 0
    for i in range(ascii_len):
        this_ch = ascii_data[i]
        if this_ch == BASE64_PAD:
            padding_started = 1
            # if(quad_pos >= 2 && quad_pos + ++pads >= 4)
            if quad_pos >= 2:
                pads += 1
                if quad_pos + pads >= 4:
                    # A pad sequence means we should not parse more input.
                    # We've already interpreted the data from the quad at this point.
                    # in strict mode, an error should raise if there's excess data after the padding
                    if strict_mode and i+1 < ascii_len:
                        raise Error('Excess data after padding')
                    return bin_data
        this_ch = TABLE_A2B_BASE64[this_ch]
        if strict_mode:
            if this_ch >= 64:
                raise Error('Only base64 data is allowed')

            # Characters that are not '=', in the middle of the padding, are not allowed
            if padding_started:
                raise Error('Discontinuous padding not allowed')
        
        pads = 0

        if quad_pos == 0:
            quad_pos = 1
            leftchar = this_ch
        elif quad_pos == 1:
            quad_pos = 2
            # *bin_data++ = ...
            bin_data[bdpos] = (leftchar << 2) | (this_ch >> 4)
            bdpos += 1
            leftchar = this_ch & 0x0f
        elif quad_pos == 2:
            quad_pos = 3
            # *bin_data++ = ...
            bin_data[bdpos] = (leftchar << 4) | (this_ch >> 2)
            bdpos += 1
            leftchar = this_ch & 0x03
        elif quad_pos == 3:
            quad_pos = 0
            # *bin_data++ = ...
            bin_data[bdpos] = (leftchar << 6) | this_ch
            bdpos += 1
            leftchar = 0
    if quad_pos != 0:
        if quad_pos == 1:
            dc = (bdpos - 1) / 3 * 4 + 1
            raise Error(f'Invalid base64 string: number of data characters ({dc}) cannot be one more than a multiple of 4')
        else:
            raise Error('Incorrect padding')
            
def binascii_b2a_base64_impl(data: bytes, newline: bool = False) -> str:
    ascii_data: bytes
    bin_data: bytes = data
    leftbits: int = 0
    leftchar: int = 0
    this_ch: int
    bin_len: int = len(bin_data)
    out_len: int

    # n: Skipping memory check because fuck it

    # We're lazy and allocate too much (fixed up later)
    # "+2" leaves room for up to two pad characters.
    # Note that 'b' gets encoded as 'Yg==\n' (1 in, 5 out).
    out_len = (bin_len * 2) + 2
    if newline:
        out_len += 1
    ascii_data = bytes(out_len)
    bdpos = 0
    adpos = 0
    while bin_len > 0:
        # Shift the data into our buffer
        leftchar = (leftchar << 8) | bin_data[bdpos]
        leftbits += 8

        # See if there are any 6-bit groups ready
        while leftbits >= 6:
            this_ch = (leftchar >> (leftbits-6)) & 0x3f
            leftbits -= 6
            ascii_data[adpos] = TABLE_B2A_BASE64[this_ch]
            adpos += 1
            
        bin_len -= 1
        bdpos += 1

    if leftbits == 2:
        ascii_data[adpos] = TABLE_B2A_BASE64[(leftchar&3)<<4]
        ascii_data[adpos+1] = BASE64_PAD
        ascii_data[adpos+2] = BASE64_PAD
        adpos += 3
    elif leftbits == 4:
        ascii_data[adpos] = TABLE_B2A_BASE64[(leftchar & 0xf) << 2]
        ascii_data[adpos + 1] = BASE64_PAD
        adpos += 2
    if newline:
        ascii_data[adpos] = b'\n' # Append a courtesy newline
    return ascii_data