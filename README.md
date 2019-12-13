# flake8-super-mario

An extension for flake8 with super_mario specific validations.

[Mario](https://github.com/best-doctor/Mario) is a framework for business
logic flow. It's best when user follows all rules.
Some rules are checked by Mario itself and some are best with
static analysis and can be checked with this plugin. 

## Installation

    pip install flake8-super-mario


## Example

```python
from super_mario import BasePipeline, process_pipe


class SimplePipeline(BasePipeline):
    pipeline = [
        'sum_numbers',
    ]

    def sum_numbers(a, b):
        return {'d': a + b}
```
Usage:

```terminal
$ flake8 test.py
text.py:1:5: SME001 Pipe sum_numbers has no pipe decorator
```


## Error codes

| Error code |                           Description               |
|:----------:|:---------------------------------------------------:|
|   SME001   | Pipe XXX has no pipe decorator                      |
|   SME002   | Pipe XXX has too high cyclomatic complexity (X > Y) |
|   SME003   | Pipe XXX has too high cognitive complexity (X > Y)  |
|   SME004   | Pipe XXX is of process type and is not pure         |
