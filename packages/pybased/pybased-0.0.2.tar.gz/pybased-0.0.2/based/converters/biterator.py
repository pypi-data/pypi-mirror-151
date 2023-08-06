# Roughly based off of Python's official system.

import math
from fractions import Fraction
from io import BytesIO, StringIO
from typing import IO, BinaryIO, Optional, TextIO, Tuple

from based.abcs import IBaseConverter
from frozendict import frozendict

__ALL__ = ['BiteratorBaseConverter']

class BiteratorBaseConverter(IBaseConverter):
    CONVERTER_TYPE_NAME = 'Biterator'
    def __init__(self, id: str, alphabet: str, padchar: Optional[str] = None) -> None:
        super().__init__(id, alphabet, padchar)
        self.bits_per_char: int = (self.length - 1).bit_length()
        self.ratio = Fraction(self.bits_per_char, 8)
        self.mask: int = (1 << self.bits_per_char) - 1
        self.pad_modulo: int = self.ratio.numerator #honk
        #print(self.id, f'ratio={self.ratio}', f'mask={self.mask:b}', f'mod={self.pad_modulo}')
        
    def encode_stream(self, inbytes: BinaryIO, output: TextIO, pad: bool = True) -> None:
        work: int = 0
        bits: int = 0
        written: int = 0
        c: int
        nb: int
        while len(nb := inbytes.read(1)) > 0:
            #print(repr(nb), bin(work), bits)
            work = (work << 8) | ord(nb)
            bits += 8
            while bits >= self.bits_per_char:
                c = (work >> (bits - self.bits_per_char)) & self.mask
                bits -= self.bits_per_char
                if c < 0 or c >= self.length:
                    raise Exception(f'{self.id}: c = {c}, len = {self.length}, bpc = {self.bits_per_char}')
                output.write(self.alphabet[c])
                written += 1
            # Clean up
            work = work % (1 << bits)
        c = 0
        if bits > 0:
            c = (work & ((1 << bits) - 1)) << (self.bits_per_char-bits)
            output.write(self.alphabet[c])
            written += 1
            if pad and self.pad_char:
                output.write(self.pad_char * self.padding_to_write(written))
        
    def decode_stream(self, inputs: TextIO, outbytes: BinaryIO) -> None:
        buffer: int = 0
        bits: int = 0
        b: int
        while len(nc := inputs.read(1)) > 0:
            if nc == self.pad_char:
                # We're in the padding.  We're done.
                return
            buffer = (buffer << self.bits_per_char) | self.c2i[nc]
            bits += self.bits_per_char
            if bits >= 8:
                b = (buffer >> (bits - 8)) & 0xff
                outbytes.write(b.to_bytes(1, 'big'))
                bits -= 8
            # Clean up
            buffer = buffer % (1 << bits)
        if bits > 0:
            b = (buffer & ((1 << bits) - 1)) << (8 - bits)
            if b>0:
                outbytes.write(b.to_bytes(1, 'big'))

    def decode_bytes(self, input: str) -> bytes:
        with StringIO(input) as inputstr, BytesIO() as outputbytes:
            self.decode_stream(inputstr,outputbytes)
            o = outputbytes.getvalue()
            return o

    def decode_int(self, input: str) -> int:
        b = self.decode_bytes(input)
        return int.from_bytes(b, 'big')

    def encode_bytes(self, data: bytes, pad: bool = True) -> str:
        with BytesIO(data) as inputbytes, StringIO() as outputstr:
            self.encode_stream(inputbytes, outputstr, pad)
            return outputstr.getvalue()

    def encode_int(self, integer: int, pad: bool = True) -> str:
        return self.encode_bytes(integer.to_bytes(integer.bit_length()//8, 'big'), pad)
