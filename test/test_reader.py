from src.reader import FileOperator


def test_file_operator():
    rf = FileOperator.read_file("../repo_files/base32.py")
    print(rf)
    FileOperator.create_file("../examples/test_file.txt")
    FileOperator.write_file("../examples/test_file.txt", "This is a test output.")


test_file_operator()
