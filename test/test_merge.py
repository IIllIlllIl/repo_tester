def merge(file_contents):
    import_statements = set()
    from_imports = set()
    non_import_code = []
    for content in file_contents:
        lines = content.split('\n')
        current_code = []

        for line in lines:
            stripped = line.strip()
            if stripped.startswith('import ') or stripped.startswith('from '):
                import_statements.add(stripped) if stripped.startswith('import ') else from_imports.add(stripped)
            else:
                current_code.append(line)

        non_import_code.append('\n'.join(current_code))

    sorted_imports = []
    sorted_imports.extend(sorted(import_statements))
    sorted_imports.extend(sorted(from_imports))

    final_imports = '\n'.join(sorted_imports)
    final_code = f"{final_imports}\n\n" + '\n\n'.join(non_import_code).strip()

    return final_code


def test_merge():
    c0 = """import pytest

def test_base32_encode():
    # Normal cases
    assert base32_encode(b"Hello World!") == b'JBSWY3DPEBLW64TMMQQQ===='
    assert base32_encode(b"123456") == b'GEZDGNBVGY======'
    assert base32_encode(b"some long complex string") == b'ONXW2ZJANRXW4ZZAMNXW24DMMV4CA43UOJUW4ZY='"""
    c2 = """import b
from a import c

def test_base32_encode_2():
    # Edge/boundary cases
    assert base32_encode(b"") == b''
    assert base32_encode(b"a") == b'ME======'
    assert base32_encode(b"ab") == b'MFRA===='
    assert base32_encode(b"abc") == b'MFRGG==='
    assert base32_encode(b"abcd") == b'MFRGGZA='
    assert base32_encode(b"abcde") == b'MFRGGZDF'"""
    m = merge([c0, c2])
    print(m)


test_merge()
