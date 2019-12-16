from conftest import run_validator_for_test_file


def test_no_errors_for_ok_pipe():
    assert not run_validator_for_test_file('ok_pipe.py')


def test_errors_for_not_ok_pipes():
    assert len(run_validator_for_test_file('fail_pipes.py')) == 3


def test_errors_for_not_pure_pipes():
    assert len(run_validator_for_test_file('non_pure_pipeline.py')) == 2
