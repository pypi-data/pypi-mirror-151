'''
Base32 implementations, the vast majority of which were gathered from https://en.wikipedia.org/w/index.php?title=Base32&oldid=1075459441

'''
import string
from typing import List

from based.abcs import IBaseConverter
from based.converters import slidingwindow
from based.converters.biterator import BiteratorBaseConverter
from based.converters.slidingwindow import SlidingWindowBaseConverter

__ALL__ = [
    'ALL',
    'base32',
    'base32hex',
    'crockford32',
    'geohash32',
    'nintendo32',
    'wordsafe32',
    'zbase32',
]

'''
def b32_check(base: SlidingWindowBaseConverter, zero_char: str) -> None:
    assert len(base.alphabet) == 32, f'{base.id} - alphabet length is not 32: {len(base.alphabet)}'
    assert base.bits_per_char == 5, f'{base.id} - bits per char is not 5: {base.bits_per_char}'
    assert base.chars_per_byte == 3, f'{base.id} - chars per byte is not 3: {base.chars_per_byte}'
    assert base.zero_char == zero_char, f'{base.id} - zero char is not {zero_char!r}: {base.zero_char!r}'
    if base.pad_char is not None:
        assert base.pad_char not in base.alphabet, f'{base.id} - pad char {base.pad_char!r} is in {base.alphabet!r}'
    return base

base32      = b32_check(SlidingWindowBaseConverter('base32',      string.ascii_uppercase + '234567', '='), 'A')  # rfc4648
base32hex   = b32_check(SlidingWindowBaseConverter('base32hex',   string.digits + string.ascii_uppercase[:22], '='), '0')  # rfc2938
crockford32 = b32_check(SlidingWindowBaseConverter('crockford32', '0123456789ABCDEFGHJKMNPQRSTVWXYZ'), '0')
geohash32   = b32_check(SlidingWindowBaseConverter('geohash32',   '0123456789bcdefghjkmnpqrstuvwxyz'), '0')
zbase32     = b32_check(SlidingWindowBaseConverter('zbase32',     'ybndrfg8ejkmcpqxot1uwisza345h769'), 'y')
# Apparently some nintendo games used some variation on this characterset? 
# TODO: Pin down some examples
nintendo32  = b32_check(SlidingWindowBaseConverter('nintendo32',  '0123456789BCDFGHJKLMNPQRSTVWXYZ?'), '0')
# Open Location Code Base32
wordsafe32  = b32_check(SlidingWindowBaseConverter('wordsafe32',  '23456789CFGHJMPQRVWXcfghjmpqrvwx'), '2')
'''


def b32_check(base: BiteratorBaseConverter, zero_char: str) -> BiteratorBaseConverter:
    assert len(base.alphabet) == 32, f'{base.id} - alphabet length is not 32: {len(base.alphabet)}'
    assert base.bits_per_char == 5, f'{base.id} - bits per char is not 5: {base.bits_per_char}'
    assert base.pad_modulo == 5, f'{base.id} - pad modulo is not 5: {base.pad_modulo}'
    assert base.zero_char == zero_char, f'{base.id} - zero char is not {zero_char!r}: {base.zero_char!r}'
    if base.pad_char is not None:
        assert base.pad_char not in base.alphabet, f'{base.id} - pad char {base.pad_char!r} is in {base.alphabet!r}'
    return base

class RFC4648Base32Converter(BiteratorBaseConverter):
    def padding_to_write(self, written_chars: int) -> int:
        return (8 - (written_chars % 8)) % 8


base32 = b32_check(RFC4648Base32Converter('base32', string.ascii_uppercase + '234567', '='), 'A')  # rfc4648
base32hex = b32_check(RFC4648Base32Converter('base32hex', string.digits + string.ascii_uppercase[:22], '='), '0')  # rfc2938
crockford32 = b32_check(BiteratorBaseConverter('crockford32', '0123456789ABCDEFGHJKMNPQRSTVWXYZ'), '0')
geohash32 = b32_check(BiteratorBaseConverter('geohash32', '0123456789bcdefghjkmnpqrstuvwxyz'), '0')
zbase32 = b32_check(BiteratorBaseConverter('zbase32', 'ybndrfg8ejkmcpqxot1uwisza345h769'), 'y')
# Apparently some nintendo games used some variation on this characterset?
# TODO: Pin down some examples
nintendo32 = b32_check(BiteratorBaseConverter('nintendo32', '0123456789BCDFGHJKLMNPQRSTVWXYZ?'), '0')
# Open Location Code Base32
wordsafe32 = b32_check(BiteratorBaseConverter('wordsafe32', '23456789CFGHJMPQRVWXcfghjmpqrvwx'), '2')

ALL: List[IBaseConverter] = [
    base32,
    base32hex,
    crockford32,
    geohash32,
    nintendo32,
    wordsafe32,
    zbase32,
]
