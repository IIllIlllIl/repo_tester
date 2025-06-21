from src.model import Model
import sys
import os


sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


def test_model():
    message = """You are a professional Python test engineer.
            Please generate at least 5 test assertions for the following Python methods.
            Requirements:
            1. analyze the method's input parameters, return values, and possible behaviors
            2. generate assertions for multiple typical test scenarios,
            including normal case, boundary case, and abnormal case
            3. use pytest style `assert` statements
            4. Do not generate the actual test code or explanations, only the assertions.
            Method information: def base32_encode(data: bytes) -> bytes:
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

    m = Model("http://localhost:8000", "v1/chat/completions", "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B", message)

    response = m.call_llm_api()
    if response:
        # 调整为chat completions的响应格式
        content = response["choices"][0]["message"]["content"]
        print(f"LLM: {content}")


test_model()

