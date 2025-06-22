import re
import sys
import os
import subprocess
from src.reader import FileOperator
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


class TestGenerator:
    """
    ** Abandoned class **
    Generates test cases based on the LLM generated assertion

    Attributes:
        answers (str): The answer of the LLM for one method under test (usually a long paragraph)
        assertions (List): The assertions provided by the LLM
        compiled (List): The assertions passed the compilation

    Methods:
        extract_assertions(): Extract assertions from the LLM answer
        test_assertions(output_path, imports): Check each assertion whether they can pass the compilation
        create_test_file(output_path, imports): Abandoned method
        execute_pytest(test_file): Run pytest to check compilation
    """
    def __init__(self, assertions):
        self.answers = assertions
        self.assertions = []
        self.compiled = []

    def extract_assertions(self):
        assert_pattern = re.compile(r'^\s*assert\s+.*?(?=\s*#|$)', re.MULTILINE)
        self.assertions = assert_pattern.findall(self.answers)
        return self.assertions

    def test_assertions(self, output_path, imports):
        if len(self.assertions) == 0:
            print("Error: No assertion generated.")
            return None
        # Create test case
        for i, assertion in enumerate(self.assertions):
            test_function = f"""
def test_{i}():
    {assertion}
        """

            # Add imports
            test_content = f"\n{''.join(test_function)}"
            for im in imports:
                test_content = f"{im}\n{test_content}"

            # Create test file
            file_path = f"{output_path[:-3]}-{i}.py"
            if FileOperator.create_file(file_path):
                FileOperator.write_file(file_path, test_content)
            else:
                continue

            # Run pytest and check compile failure
            result = self.execute_pytest(file_path)
            if result['returncode'] != 2:
                self.compiled.append(assertion)

            # Remove test cache file
            FileOperator.delete_file(file_path)

        return self.compiled

    def create_test_file(self, output_path, imports):
        if len(self.compiled) == 0:
            print("Error: No assertion pass compilation.")
            return None

        test_functions = []
        for i, assertion in enumerate(self.compiled):
            test_function = f"""
def test_{i}():
    {assertion}

                """
            test_functions.append(test_function)

        # Add imports
        test_content = f"\n{''.join(test_functions)}"
        for im in imports:
            test_content = f"{im}\n{test_content}"

        # Create test file
        if FileOperator.create_file(output_path):
            FileOperator.write_file(output_path, test_content)

        # Report
        return self.execute_pytest(output_path)

    @staticmethod
    def execute_pytest(test_file):
        try:
            result = subprocess.run(
                ['pytest', '-q', str(test_file)],
                capture_output=True,
                text=True,
                timeout=10
            )
            return {
                'stdout': result.stdout,
                'stderr': result.stderr,
                'returncode': result.returncode
            }
        except Exception as e:
            return {
                'stdout': '',
                'stderr': str(e),
                'returncode': -1
            }


