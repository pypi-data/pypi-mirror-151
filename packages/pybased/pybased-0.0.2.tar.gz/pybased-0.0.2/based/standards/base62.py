import string
from typing import List

from based.abcs import IBaseConverter
from based.converters.bigint import BigIntBaseConverter

__ALL__ = ['base62', 'ALL']


def b62_check(base: BigIntBaseConverter, zero_char: str) -> BigIntBaseConverter:
    assert len(base.alphabet) == 62, f'{base.id} - alphabet length is not 62: {len(base.alphabet)}'
    assert base.zero_char == zero_char, f'{base.id} - zero char is not {zero_char!r}: {base.zero_char!r}'
    if base.pad_char is not None:
        assert base.pad_char not in base.alphabet, f'{base.id} - pad char {base.pad_char!r} is in {base.alphabet!r}'
    return base


# https://en.wikipedia.org/w/index.php?title=Base62&oldid=1063612765
base62 = b62_check(BigIntBaseConverter('base62', string.digits + string.ascii_uppercase + string.ascii_lowercase), '0')

ALL: List[IBaseConverter] = [
    base62,
]
