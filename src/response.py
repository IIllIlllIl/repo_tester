from src.reader import FileOperator


class ResponseProcessor:
    """
    Process LLM output and generate test cases

    Attributes:
        response (str): LLM output
        output (str): Output file path
        test (str): Test file context

    Methods:
        extract_test_case(): Extract test cases from LLM answer
        save_test_case(import): Add imported packages to test cases and write to output path
    """
    def __init__(self, answer, output):
        self.response = answer
        self.output = output
        self.test = ""

    def extract_test_case(self):
        marker = "# ===== Test cases =====\n"
        marker_index = self.response.find(marker)
        if marker_index == -1:
            return ""
        content = self.response[marker_index + len(marker):]
        content = content.rstrip()
        if content.endswith("```"):
            content = content[:-3]
        self.test = content
        return self.test

    def save_test_case(self, imports):
        file = self.test
        file = imports + file
        FileOperator.write_file(self.output, file)

