# flake8-super-mario

[![Build Status](https://travis-ci.org/Melevir/flake8-super-mario.svg?branch=master)](https://travis-ci.org/Melevir/flake8-super-mario)
[![Maintainability](https://api.codeclimate.com/v1/badges/ea573c4743dbabd6debe/maintainability)](https://codeclimate.com/github/Melevir/flake8-super-mario/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/ea573c4743dbabd6debe/test_coverage)](https://codeclimate.com/github/Melevir/flake8-super-mario/test_coverage)
[![PyPI version](https://badge.fury.io/py/flake8-super-mario.svg)](https://badge.fury.io/py/flake8-super-mario)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/flake8-super-mario)

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
