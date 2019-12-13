from super_mario import BasePipeline, process_pipe


class SimplePipeline(BasePipeline):
    pipeline = [
        'sum_numbers',
        'multiply_numbers',
    ]

    @process_pipe
    @staticmethod
    def sum_numbers(a, b):
        return {'d': a + b}

    @process_pipe
    def multiply_numbers(c, d):
        return {'e': c * d}
