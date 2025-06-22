import sys
import os
import argparse
from src.file_data import File
from src.generator import TestGenerator
from src.model import Model
from src.config import Config
from src.get_repo import clone_github_repo
from src.build_file import Builder
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


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
        self.parser.add_argument('-k', '--k', type=int, default=10,
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

    # get GitHub repo & target file
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

    output = config.get('output')
    # clone_github_repo(repo_owner, repo_name, output)

    # Call LLM
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

    # Generate test and try compiling
    if len(contents) != 0:
        for con in contents:
            tg = TestGenerator(contents)
            # 没有生成一个test文件下的一个test函数
            # tg.extract_assertions()
            # output_path = os.path.join(output, file_path)
            # imports = config.get('imports')
            # tg.test_assertions(output_path, imports)
            # tg.create_test_file(output_path, imports)

