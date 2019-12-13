from conftest import run_validator_for_test_file


def test_no_errors_for_ok_pipe():
    assert not run_validator_for_test_file('ok_pipe.py')


def test_errors_for_notok_pipes():
    assert len(run_validator_for_test_file('fail_pipes.py')) == 3
