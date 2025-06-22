from src.response import ResponseProcessor
import re


def test_response_processor():
    model_output = """```python
# Function under test
def base32_encode(data: bytes) -> bytes:
    B32_CHARSET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"

    binary_data = "".join(bin(ord(d))[2:].zfill(8) for d in data.decode("utf-8"))
    binary_data = binary_data.ljust(5 * ((len(binary_data) // 5) + 1), "0")
    b32_chunks = map("".join, zip(*[iter(binary_data)] * 5))
    b32_result = "".join(B32_CHARSET[int(chunk, 2)] for chunk in b32_chunks)
    return bytes(b32_result.ljust(8 * ((len(b32_result) // 8) + 1), "="), "utf-8")

# ===== Test cases =====
import pytest

def test_base32_encode():
    # Normal cases
    assert base32_encode(b"Hello World!") == b'JBSWY3DPEBLW64TMMQQQ===='
    assert base32_encode(b"123456") == b'GEZDGNBVGY======'
    assert base32_encode(b"some long complex string") == b'ONXW2ZJANRXW4ZZAMNXW24DMMV4CA43UOJUW4ZY='

    # Edge/boundary cases
    assert base32_encode(b"") == b''
    assert base32_encode(b"a") == b'ME======'
    assert base32_encode(b"ab") == b'MFRA===='
    assert base32_encode(b"abc") == b'MFRGG==='
    assert base32_encode(b"abcd") == b'MFRGGZA='
    assert base32_encode(b"abcde") == b'MFRGGZDF'

    # Error/exception cases
    with pytest.raises(TypeError):
        base32_encode("not bytes")  # type: ignore
    with pytest.raises(TypeError):
        base32_encode(123)  # type: ignore
    with pytest.raises(AttributeError):
        base32_encode(b'\x80abc')  # invalid utf-8
```
    """

    rp = ResponseProcessor(model_output, "../examples/test_base32.py")
    print(rp.extract_test_case())
    rp.save_test_case("from base32 import base32_encode\n")
    ResponseProcessor.report_pytest("../examples/test_base32.py")


test_response_processor()
