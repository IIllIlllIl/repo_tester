import subprocess
from pathlib import Path
import sys
import os
from src.reader import FileOperator
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


class Builder:
    """
    Build files with assertions and imports

    Attributes:
        method_assertions (dict): All assertions for each method

    Methods:
        add_method_assertions(method_name, assertions): Overwrite assertions for a method
        generate_test_file(): Generate test functions
        write_down_test(output, imports): Write down file with functions and imports
        report_pytest(output): Run pytest and report the execution trace
    """
    def __init__(self):
        self.method_assertions = {}

    def add_method_assertions(self, method_name, assertions):
        self.method_assertions[method_name] = assertions

    def generate_test_file(self):
        test_content = ""

        for method_name, assertions in self.method_assertions.items():
            test_function_name = f"test_{method_name}"
            test_content += f"def {test_function_name}():\n"
            for assertion in assertions:
                test_content += f"    {assertion}\n"
            test_content += "\n"

        return test_content

    def write_down_test(self, output, imports=""):
        print(f"Writing {len(self.method_assertions)} tests to {output}")
        file = self.generate_test_file()
        file = imports + "\n\n" + file
        FileOperator.write_file(output, file)

    @staticmethod
    def report_pytest(output):
        file_path = Path(output)
        if not file_path.exists():
            raise FileNotFoundError(f"Test file write failed: {output}")

        # Build pytest cmd
        pytest_cmd = [
            sys.executable,
            "-m",
            "pytest",
            "-v",
            "-s",
            "-ra",
            "--tb=long",
            "--durations=0",
            str(file_path)
        ]

        try:
            print("Running tests...")
            result = subprocess.run(
                pytest_cmd,
                capture_output=True,
                text=True,
                check=False
            )

            # Print pytest output
            print("PYTEST STDOUT:")
            print(result.stdout)
            print("PYTEST STDERR:")
            print(result.stderr)

        except subprocess.SubprocessError as e:
            print(f"Unexpected error happened when running pytest: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")



