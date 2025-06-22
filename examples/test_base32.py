from repo_files.Python.ciphers.base32 import base32_encode
from repo_files.Python.ciphers.base32 import base32_decode
import pytest


def test_base32_encode():
    # Normal cases
    assert base32_encode(b"Hello World!") == b'JBSWY3DPEBLW64TMMQQQ===='
    assert base32_encode(b"123456") == b'GEZDGNBVGY======'
    assert base32_encode(b"some long complex string") == b'ONXW2ZJANRXW4ZZAMNXW24DMMV4CA43UOJUW4ZY='
    assert base32_encode(b"") == b''
    assert base32_encode(b"a") == b'ME======'
    assert base32_encode(b"ab") == b'MFRA===='

    # Edge/boundary cases
    assert base32_encode(b"1") == b'GE======'
    assert base32_encode(b"123") == b'GEZDG==='
    assert base32_encode(b"12345") == b'GEZDGNBV'
    assert base32_encode(b"1234567") == b'GEZDGNBVGYQ===='

    # Error/exception cases
    with pytest.raises(TypeError):
        base32_encode("not bytes")  # type: ignore
    with pytest.raises(TypeError):
        base32_encode(123)  # type: ignore
    with pytest.raises(AttributeError):
        base32_encode(None)  # type: ignore


def test_base32_decode():
    # Normal cases
    assert base32_decode(b'JBSWY3DPEBLW64TMMQQQ====') == b'Hello World!'
    assert base32_decode(b'GEZDGNBVGY======') == b'123456'
    assert base32_decode(b'ONXW2ZJANRXW4ZZAMNXW24DMMV4CA43UOJUW4ZY=') == b'some long complex string'

    # Edge/boundary cases
    assert base32_decode(b'MY======') == b'f'
    assert base32_decode(b'MZXQ====') == b'fo'
    assert base32_decode(b'MZXW6===') == b'foo'
    assert base32_decode(b'MZXW6YQ=') == b'foob'
    assert base32_decode(b'MZXW6YTB') == b'fooba'
    assert base32_decode(b'MZXW6YTBOI======') == b'foobar'

    # Error/exception cases
    with pytest.raises(TypeError):
        base32_decode('string')  # not bytes
    with pytest.raises(TypeError):
        base32_decode(123)  # not bytes
    with pytest.raises(ValueError):
        base32_decode(b'INVALID@')  # invalid base32 char
    with pytest.raises(ValueError):
        base32_decode(b'AAA=======')  # invalid padding length