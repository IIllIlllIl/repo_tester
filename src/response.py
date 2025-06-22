from src.reader import FileOperator


class ResponseProcessor:
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

