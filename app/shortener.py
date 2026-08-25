import string

ALPHABET = string.digits + string.ascii_letters
BASE = len(ALPHABET)


def encode_base62(num: int) -> str:
    if num == 0:
        return ALPHABET[0]

    chars = []
    while num > 0:
        num, rem = divmod(num, BASE)
        chars.append(ALPHABET[rem])
    return "".join(reversed(chars))


def decode_base62(code: str) -> int:
    num = 0
    for char in code:
        num = num * BASE + ALPHABET.index(char)
    return num
