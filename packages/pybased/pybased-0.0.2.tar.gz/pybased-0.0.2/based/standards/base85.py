import string
from typing import List

from based.abcs import IBaseConverter
from based.converters.bigint import BigIntBaseConverter
from based.converters.biterator import BiteratorBaseConverter

__ALL__ = ['base85', 'ALL']


def b85_check(base: BigIntBaseConverter, zero_char: str) -> BigIntBaseConverter:
    assert len(base.alphabet) == 85, f'{base.id} - alphabet length is not 85: {len(base.alphabet)}'
    assert base.zero_char == zero_char, f'{base.id} - zero char is not {zero_char!r}: {base.zero_char!r}'
    if base.pad_char is not None:
        assert base.pad_char not in base.alphabet, f'{base.id} - pad char {base.pad_char!r} is in {base.alphabet!r}'
    return base

# RFC1924
base85 = b85_check(BiteratorBaseConverter('base85', string.ascii_uppercase + string.ascii_lowercase + string.digits + '!#$%&()*+-;<=>?@^_`{|}~'), 'A') 

ALL: List[IBaseConverter] = [
    base85,
]
