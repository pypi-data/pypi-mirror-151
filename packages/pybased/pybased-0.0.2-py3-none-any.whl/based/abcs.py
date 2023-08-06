
from abc import ABC, abstractmethod
import math
from typing import Dict, Optional

from frozendict import frozendict


class IBaseConverter(ABC):
    CONVERTER_TYPE_NAME: str

    def __init__(self, id: str, alphabet: str, padchar: Optional[str] = None) -> None:
        super().__init__()
        self.id: str = id
        self.alphabet: str = alphabet
        self.length: int = len(alphabet)
        self.zero_char: str = alphabet[0]
        self.pad_char: Optional[str] = padchar
        self.c2i: Dict[str, int] = frozendict((c, i) for i, c in enumerate(self.alphabet))
        self.byte_to_char_ratio: float = 256. / float(self.length)
        self.char_to_byte_ratio: float = float(self.length) / 256.

    def get_b2a_buffer_size(self, origlen: int) -> int:
        '''
        Estimate size of buffer for bytes -> str operations.

        Deliberately overestimates.
        '''
        return math.ceil((origlen * math.log(self.length)) / math.log(256))

    def get_a2b_buffer_size(self, origlen: int) -> int:
        '''
        Estimate size of buffer for str -> bytes operations.

        Deliberately overestimates.
        '''
        return math.ceil((origlen * math.log(256)) / math.log(self.length))

    def padding_to_write(self, written_chars: int) -> int:
        return 0

    @abstractmethod
    def decode_bytes(self, input: str) -> bytes:
        pass

    @abstractmethod
    def decode_int(self, input: str) -> int:
        pass

    @abstractmethod
    def encode_bytes(self, data: bytes, pad: bool = True) -> str:
        pass

    @abstractmethod
    def encode_int(self, integer: int, pad: bool = True) -> str:
        pass
