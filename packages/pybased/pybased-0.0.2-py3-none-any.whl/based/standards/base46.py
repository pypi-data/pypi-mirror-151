from typing import List
from based.abcs import IBaseConverter
from based.converters.bigint import BigIntBaseConverter
from based.converters.biterator import BiteratorBaseConverter


def b46_check(base: BigIntBaseConverter, zero_char: str) -> BigIntBaseConverter:
    assert len(base.alphabet) == 46, f'{base.id} - alphabet length is not 46: {len(base.alphabet)}'
    assert base.zero_char == zero_char, f'{base.id} - zero char is not {zero_char!r}: {base.zero_char!r}'
    if base.pad_char is not None:
        assert base.pad_char not in base.alphabet, f'{base.id} - pad char {base.pad_char!r} is in {base.alphabet!r}'
    return base
    

base46 = b46_check(BigIntBaseConverter('base46', 'ABCDEFGHJKMNPQRSTUVWXYZabcdefghjkmnpqrstuvwxyz'), 'A')

ALL: List[IBaseConverter] = [
    base46,
]