import pytest

test_data = [{"test_input": "3+5",
              "expected": 8,
              "id": "验证3+5=8"
              },
             {"test_input": "2+4",
              "expected": 6,
              "id": "验证2+4=6"
              },
             {"test_input": "6 * 9",
              "expected": 42,
              "id": "验证6*9=42"
              }
             ]


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
    ids = []
    if "parameters" in metafunc.fixturenames:
        for data in test_data:  # 用test_data中的id作为测试用例名称
            ids.append(data['id'])
        metafunc.parametrize("parameters", test_data, ids=ids, scope="function")  # 用test_data这个列表对parameters进行参数化
