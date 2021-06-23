import pytest
from utils.request import RequestUtil

requestUtil = RequestUtil()


def test_apis(parameters: dict):
    title = parameters.pop('title')
    url = parameters.pop('url')
    method = parameters.pop('method')
    jsonpath_exp_save = parameters.pop('jsonpath_exp_save')
    regular_exp_save = parameters.pop('regular_exp_save')
    jsonpath_exp_assertion = parameters.pop('jsonpath_exp_assertion')
    regular_exp_assertion = parameters.pop('regular_exp_assertion')
    requestUtil.send_request(method, url, title, jsonpath_exp_save=jsonpath_exp_save, regular_exp_save=regular_exp_save,
                             jsonpath_exp_assertion=jsonpath_exp_assertion, regular_exp_assertion=regular_exp_assertion,
                             **parameters)


if __name__ == '__main__':
    pytest.main(['-s', '-x', 'test_pytest.py'])
