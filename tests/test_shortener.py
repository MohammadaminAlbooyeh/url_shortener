from app.shortener import decode_base62, encode_base62


def test_encode_zero():
    assert encode_base62(0) == "0"


def test_encode_basic():
    assert encode_base62(1) == "1"
    assert encode_base62(10) == "a"
    assert encode_base62(62) == "10"


def test_decode_basic():
    assert decode_base62("1") == 1
    assert decode_base62("a") == 10
    assert decode_base62("10") == 62


def test_roundtrip():
    for value in [0, 1, 61, 62, 63, 1000, 999999, 123456789]:
        assert decode_base62(encode_base62(value)) == value


def test_encode_unique():
    codes = {encode_base62(i) for i in range(10000)}
    assert len(codes) == 10000
