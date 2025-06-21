import src.file_data as fd


def test_file():
    f = fd.File("TheAlgorithms", "Python", "ciphers/base32.py", "master")
    f.extract_methods()
    f.display()
    m = f.prompting(10)
    print(m)


test_file()
