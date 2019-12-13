import ast
from mccabe import PathGraphingAstVisitor


def get_cyclomatic_complexity(some_funcdef: ast.FunctionDef) -> int:
    visitor = PathGraphingAstVisitor()
    visitor.preorder(some_funcdef, visitor)
    return list(visitor.graphs.values())[0].complexity()
