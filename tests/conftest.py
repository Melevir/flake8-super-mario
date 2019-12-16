import ast
import os
from typing import List

from flake8_super_mario.checker import SuperMarionChecker


def run_validator_for_test_file(filename: str) -> List:
    test_file_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'test_files',
        filename,
    )
    with open(test_file_path, 'r') as file_handler:
        raw_content = file_handler.read()
    tree = ast.parse(raw_content)
    checker = SuperMarionChecker(tree=tree, filename=test_file_path)

    return list(checker.run())
