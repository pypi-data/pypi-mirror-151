import math
from typing import Literal, Optional

from based.abcs import IBaseConverter

__ALL__ = ['BigIntBaseConverter']


class BigIntBaseConverter(IBaseConverter):
    CONVERTER_TYPE_NAME = 'BigInt'

    def __init__(self, id: str, alphabet: str, padchar: Optional[str] = None, pad_divisor: Optional[int] = None, endianness: Literal['big', 'little'] = 'big') -> None:
        super().__init__(id, alphabet, padchar)
        self.pad_divisor: Optional[int] = pad_divisor
        self.endianness: Literal['big', 'little'] = endianness

    def encode_bytes(self, data: bytes, pad: bool = True) -> str:
        return self.encode_int(int.from_bytes(data, byteorder=self.endianness, signed=False), pad=pad)

    def encode_int(self, integer: int, pad: bool = True) -> str:
        if integer == 0:
            return self.zero_char

        ret = ''
        while integer != 0:
            ret = self.alphabet[integer % self.length] + ret
            integer //= self.length

        if ret != '' and pad and self.pad_divisor and self.pad_char:
            ret += self.pad_char * (len(ret) % self.pad_divisor)

        return ret

    def decode_int(self, input: str) -> int:
        if self.pad_char and self.pad_divisor:
            input = input.rstrip(self.pad_char)
            
        ret: int = 0
        for i, c in enumerate(input[::-1]):
            ret += (self.length ** i) * self.c2i[c]
        return ret

    def decode_bytes(self, input: str) -> bytes:
        i: int = self.decode_int(input)
        return i.to_bytes(math.ceil(i.bit_length() / 8.), self.endianness)
