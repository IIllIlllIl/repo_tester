from src.generator import TestGenerator
import sys
import os


sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


def test_test_generator(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
    except FileNotFoundError:
        print(f"Error: file not found: '{file_path}'")
        sys.exit(1)
    except Exception as e:
        print(f"Error: Unexpected error when reading the file: {e}")
        sys.exit(1)
    tg = TestGenerator(content)
    a = tg.extract_assertions()
    print(a)
    c = tg.test_assertions("../repo_files/test_output.py",
                           ["from base32 import base32_encode", "from base32 import base32_decode"])
    print(c)
    r = tg.create_test_file("../repo_files/test_base32.py",
                            ["from base32 import base32_encode", "from base32 import base32_decode"])
    print(r)


test_test_generator("../examples/llm_answer.txt")
