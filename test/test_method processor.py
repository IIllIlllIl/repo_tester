from src.file_data import File
from src.method_processor import Method


def test_method():
    f = File("TheAlgorithms", "Python", "ciphers/base32.py", "master")
    f.extract_methods()
    m = Method(f.methods[0]['name'], f.methods[0]['class'], f.methods[0]['text'])
    m.display()


test_method()
