from base32 import base32_decode
from base32 import base32_encode


def test_0():
    assert base32_encode("Hello World!") == b'JBSWY3DPEBLW64TMMQQQ====', "Normal case - 'Hello World!' encoded correctly."

                
def test_1():
    assert base32_encode("123456") == b'GEZDGNBVGY======', "Boundary case - '123456' encoded correctly."

                
def test_2():
    assert base32_encode(b"some long complex string") == b'ONXW2ZJANRXW4ZZAMNXW24DMMV4CA43UOJUW4ZY=', "Boundary case - 'some long complex string' encoded correctly."

                
def test_3():
    assert base32_encode(b"any length") == b'KQ==', "Abnormal case - Input of length 1 results in padded '=' characters."

                