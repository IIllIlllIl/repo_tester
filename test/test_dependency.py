from src.dependency import Dependency


def test_dependency():
    file_content = """
import math
from calculator import add

def test_addition():
    result = add(1, 2)
    assert result == 3
    """
    additional_imports = ["import pytest", "from utils import helper"]
    d = Dependency(file_content, additional_imports)
    i = d.generate_imports()
    print(i)
    print(Dependency.path_to_import("../repo_files/Python/ciphers/test_base32.py"))


test_dependency()
