from super_mario import BasePipeline, process_pipe
from conftest import non_pure_function_from_another_module


def non_pure_function(a):
    print(a)
    return a


class Simple2Pipeline(BasePipeline):
    pipeline = [
        'sum_numbers',
    ]

    @process_pipe
    def sum_numbers(a, b):
        return {'d': non_pure_function(a + b)}


class Simple3Pipeline(BasePipeline):
    pipeline = [
        'sum_numbers',
    ]

    @process_pipe
    def sum_numbers(a, b):
        return {'d': non_pure_function_from_another_module(a + b)}
