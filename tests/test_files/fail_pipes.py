from super_mario import BasePipeline, process_pipe, input_pipe


class SimplePipeline(BasePipeline):
    pipeline = [
        'sum_numbers',
        'multiply_numbers',
    ]

    @process_pipe
    def sum_numbers(a, b):
        return {'d': a + b}


class Simple2Pipeline(BasePipeline):
    pipeline = [
        'sum_numbers',
    ]

    def sum_numbers(a, b):
        return {'d': a + b}


class ComplexPipeline(BasePipeline):
    pipeline = [
        'sum_numbers',
    ]

    @input_pipe
    def sum_numbers(a, b):
        if a:
            if b:
                if a + b > 0:
                    if a - b < 0:
                        return {'d': a + b}
