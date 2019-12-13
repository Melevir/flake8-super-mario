import ast
from functools import partial
from typing import Generator, Tuple, Callable, List

from cognitive_complexity.api import get_cognitive_complexity
from mr_proper.public_api import is_function_pure

from flake8_super_mario import __version__ as version
from flake8_super_mario.utils._ast import (
    get_all_pipeline_classes, get_all_pipes_from, has_any_decorator,
)
from flake8_super_mario.utils.complexity import get_cyclomatic_complexity


class SuperMarionChecker:
    IO_DECORATOR_NAMES = {'input_pipe', 'output_pipe'}
    PROCESS_DECORATOR_NAME = 'process_pipe'
    ALLOWED_DECORATOR_NAMES = {*IO_DECORATOR_NAMES, PROCESS_DECORATOR_NAME}

    DEFAULT_MAX_IO_PIPE_COGNITIVE_COMPLEXITY = 4
    DEFAULT_MAX_IO_PIPE_CYCLOMATIC_COMPLEXITY = 3

    name = 'flake8-super-mario'
    version = version

    max_io_pipe_cognitive_complexity = DEFAULT_MAX_IO_PIPE_COGNITIVE_COMPLEXITY
    max_io_pipe_cyclomatic_complexity = DEFAULT_MAX_IO_PIPE_CYCLOMATIC_COMPLEXITY

    def __init__(self, tree, filename: str):
        self.filename = filename
        self.tree = tree

    @classmethod
    def add_options(cls, parser) -> None:
        parser.add_option(
            '--max-io-pipe-cognitive-complexity',
            type=int,
            default=cls.DEFAULT_MAX_IO_PIPE_COGNITIVE_COMPLEXITY,
            parse_from_config=True,
        )
        parser.add_option(
            '--max-io-pipe-cyclomatic-complexity',
            type=int,
            default=cls.DEFAULT_MAX_IO_PIPE_CYCLOMATIC_COMPLEXITY,
            parse_from_config=True,
        )

    @classmethod
    def parse_options(cls, options) -> None:
        cls.max_io_pipe_cognitive_complexity = int(options.max_io_pipe_cognitive_complexity)
        cls.max_io_pipe_cyclomatic_complexity = int(options.max_io_pipe_cyclomatic_complexity)

    @classmethod
    def check_all_pipes_has_pipe_decorator(
        cls,
        pipeline_classdef: ast.ClassDef,
    ) -> Generator[Tuple[int, int, str], None, None]:
        for pipe_funcdef in get_all_pipes_from(pipeline_classdef):
            if not has_any_decorator(pipe_funcdef, cls.ALLOWED_DECORATOR_NAMES):
                yield (
                    pipe_funcdef.lineno,
                    pipe_funcdef.col_offset,
                    f'SME001 Pipe {pipe_funcdef.name} has no pipe decorator',
                )

    @classmethod
    def check_io_pipes_complexity(
        cls,
        pipeline_classdef: ast.ClassDef,
        max_io_pipe_cyclomatic_complexity: int,
        max_io_pipe_cognitive_complexity: int,
    ) -> Generator[Tuple[int, int, str], None, None]:
        for pipe_funcdef in get_all_pipes_from(pipeline_classdef):
            if not has_any_decorator(pipe_funcdef, cls.IO_DECORATOR_NAMES):
                continue
            cyclomatic_complexity = get_cyclomatic_complexity(pipe_funcdef)
            if cyclomatic_complexity > max_io_pipe_cyclomatic_complexity:
                yield (
                    pipe_funcdef.lineno,
                    pipe_funcdef.col_offset,
                    (
                        f'SME002 Pipe {pipe_funcdef.name} has too high cyclomatic complexity '
                        f'({cyclomatic_complexity} > {max_io_pipe_cyclomatic_complexity})'
                    ),
                )
            cognitive_complexity = get_cognitive_complexity(pipe_funcdef)
            if cognitive_complexity > max_io_pipe_cognitive_complexity:
                yield (
                    pipe_funcdef.lineno,
                    pipe_funcdef.col_offset,
                    (
                        f'SME003 Pipe {pipe_funcdef.name} has too high cognitive complexity '
                        f'({cognitive_complexity} > {max_io_pipe_cognitive_complexity})'
                    ),
                )

    @classmethod
    def check_process_pipes_are_pure(
        cls,
        pipeline_classdef: ast.ClassDef,
        ast_tree: ast.Module,
    ) -> Generator[Tuple[int, int, str], None, None]:
        for pipe_funcdef in get_all_pipes_from(pipeline_classdef):
            is_pure, errors = is_function_pure(pipe_funcdef, ast_tree, with_errors=True)
            if not is_pure:
                yield (
                    pipe_funcdef.lineno,
                    pipe_funcdef.col_offset,
                    (
                        f'SME004 Pipe {pipe_funcdef.name} is of process type and is not '
                        f'pure ({", ".join(errors)})'
                    ),
                )

    def run(self) -> Generator[Tuple[int, int, str, type], None, None]:
        tree_processors: List[Callable] = [
            self.check_all_pipes_has_pipe_decorator,
            partial(
                self.check_io_pipes_complexity,
                max_io_pipe_cyclomatic_complexity=self.max_io_pipe_cyclomatic_complexity,
                max_io_pipe_cognitive_complexity=self.max_io_pipe_cognitive_complexity,
            ),
            partial(
                self.check_process_pipes_are_pure,
                ast_tree=self.tree,
            ),
        ]
        for pipeline_classdef in get_all_pipeline_classes(self.tree):
            for processor in tree_processors:
                for lineno, offset, error_text in processor(pipeline_classdef):
                    yield (lineno, offset, error_text, type(self))
