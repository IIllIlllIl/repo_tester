from src.model import Model
import sys
import os


sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


def test_model():
    message = """Generate Python unit test code strictly following these requirements:
1. **Output Format**: Wrap the entire code in a Markdown Python code block (```python ... ```)
2. **Testing Framework**: Use pytest (not unittest)
3. **Test Organization**:
   - Structure tests as ONE function (no test classes)
   - Group by scenario in one function:
     ```python
     def test_{function_name}:
        # Normal cases
        ...
        # Edge/boundary cases
        ...
        # Error/exception cases
        ...
     ```
4. **Type Safety**:
   - All test parameters must match the function's type annotations
   - Validate type errors using `pytest.raises(TypeError)`
   - Include parameterized tests where appropriate
5. **Complete Structure**:
   ```python
   # Function under test (include definition)
   def target_function(...): ...
   
   # ===== Test cases  =====
   import pytest
   from {model_name} import {function_name}
   
   def test_{function_name}():
        # Normal cases
        ...
        # Edge/boundary cases
        ...
        # Error/exception cases
        ...
6. Purity: Output ONLY the Markdown code block with no additional text.
Function to test:
    \"\"\"
    >>> base32_encode(b"Hello World!")
    b'JBSWY3DPEBLW64TMMQQQ===='
    >>> base32_encode(b"123456")
    b'GEZDGNBVGY======'
    >>> base32_encode(b"some long complex string")
    b'ONXW2ZJANRXW4ZZAMNXW24DMMV4CA43UOJUW4ZY='
    \"\"\"
    binary_data = "".join(bin(ord(d))[2:].zfill(8) for d in data.decode("utf-8"))
    binary_data = binary_data.ljust(5 * ((len(binary_data) // 5) + 1), "0")
    b32_chunks = map("".join, zip(*[iter(binary_data)] * 5))
    b32_result = "".join(B32_CHARSET[int(chunk, 2)] for chunk in b32_chunks)
    return bytes(b32_result.ljust(8 * ((len(b32_result) // 8) + 1), "="), "utf-8")"""

    key = "sk-?"
    m = Model("https://api.deepseek.com", "deepseek-chat", message, key)

    response = m.openai_api()
    print(response)


test_model()

