from src.get_repo import get_github_file


def test_get_github_file():
    # https://github.com/TheAlgorithms/Python.git
    content = get_github_file("TheAlgorithms", "Python", "ciphers/base32.py", "master")
    print(content)


test_get_github_file()
