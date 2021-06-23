import pytest
from utils.excel import *
import os

base_dir = os.path.dirname(__file__)


@pytest.fixture(scope="function", autouse=True)
def setup_fixture():
    print("setup...")


def pytest_collection_modifyitems(items):
    """
    修改用例名称中文乱码
    :param items:
    :return:
    """
    for item in items:
        item.name = item.name.encode('utf-8').decode('unicode_escape')
        item._nodeid = item.nodeid.encode('utf-8').decode('unicode_escape')


def pytest_generate_tests(metafunc):
    """
    参数化测试用例
    :param metafunc:
    :return:
    """
    ids = []
    if "parameters" in metafunc.fixturenames:
        path = os.path.join(base_dir, 'data/test.xlsx')  # 路径拼接
        wb = load_excel(path)
        test_data = get_sheet_data(wb, name='Sheet1')
        for data in test_data:  # 用test_data中的id作为测试用例名称
            ids.append(data['title'])
        metafunc.parametrize("parameters", test_data, ids=ids, scope="function")  # 用test_data这个列表对parameters进行参数化
