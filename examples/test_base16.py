from repo_files.Python.ciphers.base16 import base16_decode
from repo_files.Python.ciphers.base16 import base16_encode
import pytest


def test_base16_encode():
    # Normal cases
    assert base16_encode(b'Hello World!') == '48656C6C6F20576F726C6421'
    assert base16_encode(b'HELLO WORLD!') == '48454C4C4F20574F524C4421'
    assert base16_encode(b'\x00\xFF') == '00FF'
    assert base16_encode(b'123') == '313233'

    # Edge/boundary cases
    assert base16_encode(b'') == ''
    assert base16_encode(b'\x00') == '00'
    assert base16_encode(b'\xFF') == 'FF'

    # Error/exception cases
    with pytest.raises(TypeError):
        base16_encode('string')  # Not bytes
    with pytest.raises(TypeError):
        base16_encode(123)  # Not bytes
    with pytest.raises(TypeError):
        base16_encode([1, 2, 3])  # Not bytes


def test_base16_decode():
    # Normal cases
    assert base16_decode('48656C6C6F20576F726C6421') == b'Hello World!'
    assert base16_decode('48454C4C4F20574F524C4421') == b'HELLO WORLD!'
    assert base16_decode('') == b''

    # Edge/boundary cases
    assert base16_decode('00') == b'\x00'
    assert base16_decode('FF') == b'\xff'
    assert base16_decode('00010203040506070809') == bytes(range(10))

    # Error/exception cases
    with pytest.raises(ValueError) as excinfo:
        base16_decode('486')
    assert "Data does not have an even number of hex digits" in str(excinfo.value)

    with pytest.raises(ValueError) as excinfo:
        base16_decode('48656c6c6f20576f726c6421')
    assert "Data is not uppercase hex or it contains invalid characters" in str(excinfo.value)

    with pytest.raises(ValueError) as excinfo:
        base16_decode('This is not base64 encoded data.')
    assert "Data is not uppercase hex or it contains invalid characters" in str(excinfo.value)

    with pytest.raises(TypeError):
        base16_decode(123)  # type: ignore