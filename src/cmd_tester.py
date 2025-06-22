import os
import argparse
import subprocess
from pathlib import Path
import sys
from src.file_data import File
from src.model import Model
from src.config import Config
from src.get_repo import clone_github_repo
from src.response import ResponseProcessor
from src.dependency import Dependency
from src.reader import FileOperator
from src.build_file import Builder


class ArgParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description=' a python program that generates and runs tests for a given python program file',
            epilog='E.g.: python cmd_tester.py'
        )
        self._add_arguments()
        self.args = None

    def _add_arguments(self):
        self.parser.add_argument('-c', '--config_path', type=str, default="../config/example.json",
                                 help='Set config file path, using "../config/example.json" as default.')

    def parse(self, args=None):
        self.args = self.parser.parse_args(args)
        return self.args

    def get_args(self):
        return self.args


if __name__ == "__main__":
    parser = ArgParser()
    options = parser.parse()
    config = Config(options.config_path)

    # Build test file path
    repo_owner = config.get('repo_owner')
    repo_name = config.get('repo_name')
    file_path = config.get('file_path')
    branch = config.get('branch')
    token = config.get('token')
    output = config.get('output')
    target_path = output_path = os.path.join(output, repo_name, file_path)
    directory = os.path.dirname(target_path)
    base_name = os.path.splitext(os.path.basename(target_path))[0]
    test_file_name = f"test_{base_name}.py"
    test_file_output_path = os.path.join(directory, test_file_name)

    # Get file under test & clone repo
    if token == "None":
        token = None
    f = File(repo_owner, repo_name, file_path, branch, token)
    f.extract_methods()
    prompt_messages = f.prompting(base_name)
    methods = f.get_method_names()
    clone_github_repo(repo_owner, repo_name, output)

    # Get imports
    imports = config.get('imports')
    model_name = Dependency.path_to_import(target_path)
    for m in methods:
        imports.append(f"from {model_name} import {m}")
    d = Dependency(f.content, imports)
    imp = d.generate_imports()

    # Call LLM and get test
    based_url = config.get('based_url')
    relative_url = config.get('relative_url')
    model = config.get('model')
    temperature = config.get('temperature')
    key = config.get('key')

    contents = []
    print("Calling LLM API...")
    for message in prompt_messages:
        m = Model(based_url, model, message, key, temperature)
        response = m.openai_api()
        rp = ResponseProcessor(response, test_file_output_path)
        rp.extract_test_case()
        contents.append(rp.test)

    # Save file and run pytest
    merged_content = Builder.merge(contents)
    test_file_content = imp + "\n" + Builder.remove_imports(merged_content, base_name)
    print(f"Write {len(contents)} tests to {test_file_output_path}.")
    FileOperator.write_file(test_file_output_path, test_file_content)
    Builder.report_pytest(test_file_output_path)
