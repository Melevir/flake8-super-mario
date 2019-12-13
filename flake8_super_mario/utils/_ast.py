import ast
from typing import List, Set


def get_all_pipeline_classes(
    ast_tree: ast.Module,
    base_pipeline_class_name: str = 'BasePipeline',
) -> List[ast.ClassDef]:
    if not is_module_has_pipeline_class_import(ast_tree, base_pipeline_class_name):
        return []

    pipeline_classes: List[ast.ClassDef] = []
    for classdef_node in [n for n in ast.walk(ast_tree) if isinstance(n, ast.ClassDef)]:
        bases_names = [a.id for a in classdef_node.bases if isinstance(a, ast.Name)]
        if base_pipeline_class_name in bases_names:
            pipeline_classes.append(classdef_node)
    return pipeline_classes


def is_module_has_pipeline_class_import(
    ast_tree: ast.AST,
    base_pipeline_class_name: str,
) -> bool:
    has_pipeline_class_import = False
    for import_node in [n for n in ast.walk(ast_tree) if isinstance(n, ast.ImportFrom)]:
        if (
            import_node.module == 'super_mario'
            and base_pipeline_class_name in (n.name for n in import_node.names)
        ):
            has_pipeline_class_import = True
    return has_pipeline_class_import


def get_all_pipes_from(
    pipeline: ast.ClassDef,
    pipeline_argument_name: str = 'pipeline',
) -> List[ast.FunctionDef]:
    assigns = [
        a for a in pipeline.body
        if (
            isinstance(a, ast.Assign)
            and len(a.targets) == 1
            and getattr(a.targets[0], 'id', None) == pipeline_argument_name
            and isinstance(a.value, ast.List)
            and all(isinstance(c, ast.Constant) for c in a.value.elts)
        )
    ]
    if not assigns:
        return []

    funcdefs_map = {n.name: n for n in pipeline.body if isinstance(n, ast.FunctionDef)}

    pipes: List[ast.FunctionDef] = []
    for pipe_name in [c.value for c in assigns[0].value.elts]:  # type: ignore
        pipe_funcdef = funcdefs_map.get(pipe_name)
        if pipe_funcdef:
            pipes.append(pipe_funcdef)
    return pipes


def has_any_decorator(any_funcdef: ast.FunctionDef, decorator_names: Set[str]) -> bool:
    existing_decorators = {d.id for d in any_funcdef.decorator_list if isinstance(d, ast.Name)}
    return bool(existing_decorators.intersection(decorator_names))
