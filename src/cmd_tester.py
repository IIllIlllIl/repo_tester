import sys
import os
import argparse
from src.file_data import File
from src.generator import TestGenerator
from src.model import Model
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
        self.parser.add_argument('-n', '--number', type=int, default=10, help='指定数字 (默认: 10)')

    def parse(self, args=None):
        self.args = self.parser.parse_args(args)
        return self.args

    def get_args(self):
        return self.args


if __name__ == "__main__":
    parser = ArgParser()
    options = parser.parse()

