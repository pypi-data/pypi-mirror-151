from typing import List
from based.abcs import IBaseConverter
from based.converters.bigint import BigIntBaseConverter

__ALL__ = ['base94', 'ALL']

# Custom encoding I made for my own devious purposes.
#alphabet = ''.join(sorted(string.ascii_uppercase+string.ascii_lowercase+string.digits+'`!@#$%^&*()-=~_+{}[]:";\',./<>?\\|', key=ord))


def b94_check(base: BigIntBaseConverter, zero_char: str) -> BigIntBaseConverter:
    assert len(base.alphabet) == 94, f'{base.id} - alphabet length is not 94: {len(base.alphabet)}'
    assert base.zero_char == zero_char, f'{base.id} - zero char is not {zero_char!r}: {base.zero_char!r}'
    if base.pad_char is not None:
        assert base.pad_char not in base.alphabet, f'{base.id} - pad char {base.pad_char!r} is in {base.alphabet!r}'
    return base

base94 = b94_check(BigIntBaseConverter('base94', '!"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~'), '!')

ALL: List[IBaseConverter] = [base94]