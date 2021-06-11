import pytest


def test_001():
    print("test_001")


def test_002():
    print("test_002")


def test_eval(parameters):
    assert eval(parameters['test_input']) == parameters['expected']


if __name__ == '__main__':
    pytest.main(['-s', ' test_pytest.py'])
