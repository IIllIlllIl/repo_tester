from src.get_repo import get_github_file
from src.get_repo import clone_github_repo


def test_get_github_file():
    # https://github.com/TheAlgorithms/Python.git
    content = get_github_file("TheAlgorithms", "Python", "ciphers/base32.py", "master")
    print(content)


def test_clone_github_repo():
    clone_github_repo("IIllIlllIl", "os", "../repo_files/")


test_get_github_file()
# test_clone_github_repo()
