from super_mario import BasePipeline, process_pipe


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
