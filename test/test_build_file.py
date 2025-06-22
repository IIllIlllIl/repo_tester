from src.build_file import Builder


def test_builder():
    as_fun0 = ["assert a = b", "assert b = c"]
    as_fun1 = ["assert c = d"]
    b = Builder()
    b.add_method_assertions("func0", as_fun0)
    b.add_method_assertions("func1", as_fun1)
    f = b.generate_test_file()
    print(f)
    b.write_down_test("../examples/test_builder.py", "import a\nimport b")


test_builder()
