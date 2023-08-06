from typing import List

from based.abcs import IBaseConverter
from based.converters.bigint import BigIntBaseConverter
from based.converters.biterator import BiteratorBaseConverter
from based.converters.slidingwindow import SlidingWindowBaseConverter

__ALL__ = [
    'ALL',
    'base64',
    'base64b64',
    'base64bash',
    'base64bcrypt',
    'base64hqx',
    'base64url',
    'base64uu',
    'base64xx',
]


def b64_check(base: BiteratorBaseConverter, zero_char: str) -> BiteratorBaseConverter:
    assert len(base.alphabet) == 64, f'{base.id} - alphabet length is not 64: {len(base.alphabet)}'
    assert base.bits_per_char == 6, f'{base.id} - bits per char is not 6: {base.bits_per_char}'
    assert base.pad_modulo == 3, f'{base.id} - pad_modulo is not 3: {base.pad_modulo}'
    assert base.zero_char == zero_char, f'{base.id} - zero char is not {zero_char!r}: {base.zero_char!r}'
    if base.pad_char is not None:
        assert base.pad_char not in base.alphabet, f'{base.id} - pad char {base.pad_char!r} is in {base.alphabet!r}'
    return base
    
class RFC4648Base64Converter(BiteratorBaseConverter):
    def padding_to_write(self, written_chars: int) -> int:
        return 4 - (written_chars % 4)

# https://en.wikipedia.org/w/index.php?title=Base64&oldid=1083790400
# rfc4648
base64 = b64_check(RFC4648Base64Converter('base64', 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/', '='), 'A')
base64b64 = b64_check(RFC4648Base64Converter('base64b64', './0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz', '='), '.')
base64bash = b64_check(RFC4648Base64Converter('base64bash', '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ@_', '='), '0')
base64bcrypt = b64_check(RFC4648Base64Converter('base64bcrypt', './ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789', '='), '.')
base64hqx = b64_check(RFC4648Base64Converter('base64hqx', '!"#$%&\'()*+,-012345689@ABCDEFGHIJKLMNPQRSTUVXYZ[`abcdefhijklmpqr', '='), '!')
base64url = b64_check(RFC4648Base64Converter('base64url', 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_', '='), 'A')
base64uu = b64_check(RFC4648Base64Converter('base64uu', ' !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_'), ' ')
base64xx = b64_check(RFC4648Base64Converter('base64xx', '+-0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz', '='), '+')
'''
def b64_check(base: BigIntBaseConverter, zero_char: str) -> None:
    assert len(base.alphabet) == 64, f'{base.id} - alphabet length is not 64: {len(base.alphabet)}'
    #assert base.bits_per_char == 6, f'{base.id} - bits per char is not 6: {base.bits_per_char}'
    #assert base.chars_per_byte == 3, f'{base.id} - chars per byte is not 3: {base.chars_per_byte}'
    assert base.zero_char == zero_char, f'{base.id} - zero char is not {zero_char!r}: {base.zero_char!r}'
    return base

# https://en.wikipedia.org/w/index.php?title=Base64&oldid=1083790400
# rfc4648
base64 = b64_check(BigIntBaseConverter('base64', 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/', '=', 3), 'A')
base64b64 = b64_check(BigIntBaseConverter('base64b64', './0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz', '=', 3), '.')
base64bash = b64_check(BigIntBaseConverter('base64bash', '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ@_', '=', 3), '0')
base64bcrypt = b64_check(BigIntBaseConverter('base64bcrypt', './ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789', '=', 3), '.')
base64hqx = b64_check(BigIntBaseConverter('base64hqx', '!"#$%&\'()*+,-012345689@ABCDEFGHIJKLMNPQRSTUVXYZ[`abcdefhijklmpqr', '=', 3), '!')
base64url = b64_check(BigIntBaseConverter('base64url', 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_', '=', 3), 'A')
base64uu = b64_check(BigIntBaseConverter('base64uu', ' !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_', '=', 3), ' ')
base64xx = b64_check(BigIntBaseConverter('base64xx', '+-0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz', '=', 3), '+')
'''

ALL: List[IBaseConverter] = [
    base64,
    base64b64,
    base64bash,
    base64bcrypt,
    base64hqx,
    base64url,
    base64uu,
    base64xx,
]
