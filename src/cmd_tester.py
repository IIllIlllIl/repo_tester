import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import argparse
from src.file_data import File
from src.generator import TestGenerator
from src.model import Model
from src.config import Config
from src.get_repo import clone_github_repo
from src.build_file import Builder
from src.dependency import Dependency


class ArgParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description=' a python program that generates and runs tests for a given python program file',
            epilog='E.g.: python cmd_tester.py'
        )
        self._add_arguments()
        self.args = None

    def _add_arguments(self):
        self.parser.add_argument('-c', '--config_path', type=str, default="config/example.json",
                                 help='Set config file path, using "config/example.json" as default.')
        self.parser.add_argument('-k', '--k', type=int, default=3,
                                 help='Set the time of LLM generation. The assertions involved in the final test'
                                      'case will less than k, since some do not pass the compilation.')

    def parse(self, args=None):
        self.args = self.parser.parse_args(args)
        return self.args

    def get_args(self):
        return self.args


if __name__ == "__main__":
    parser = ArgParser()
    options = parser.parse()
    config = Config(options.config_path)

    # Get file under test
    repo_owner = config.get('repo_owner')
    repo_name = config.get('repo_name')
    file_path = config.get('file_path')
    branch = config.get('branch')
    token = config.get('token')
    if token == "None":
        token = None
    f = File(repo_owner, repo_name, file_path, branch, token)
    f.extract_methods()
    prompt_messages = f.prompting(options.k)
    methods = f.get_method_names()

    # Get imports
    imports = config.get('imports')
    d = Dependency(f.content, imports)
    imp = d.generate_imports()

    # Clone repo
    output = config.get('output')
    clone_github_repo(repo_owner, repo_name, output)

    # Build test file path
    target_path = output_path = os.path.join(output, repo_name, file_path)
    directory = os.path.dirname(target_path)
    base_name = os.path.splitext(os.path.basename(target_path))[0]
    test_file_name = f"test_{base_name}.py"
    test_file_output_path = os.path.join(directory, test_file_name)

    # Call LLM and get assertions
    based_url = config.get('based_url')
    relative_url = config.get('relative_url')
    model = config.get('model')
    temperature = config.get('temperature')
    contents = []
    for message in prompt_messages:
        m = Model(based_url, relative_url, model, message, temperature)
        response = m.call_llm_api()
        if response:
            contents.append(response["choices"][0]["message"]["content"])
        else:
            contents.append(None)

    # Generate test and try compiling
    assertions = {}
    for m, c in zip(methods, contents):
        if c is not None:
            tg = TestGenerator(c)
            tg.extract_assertions()
            # Try compile
            compiled = tg.test_assertions(test_file_output_path, imp)
            assertions[m] = compiled

    # Build files with assertions passed compilation
    b = Builder()
    for m, c in assertions:
        b.add_method_assertions(m, c)
    b.write_down_test(test_file_output_path, imp)
    b.report_pytest(test_file_output_path)
