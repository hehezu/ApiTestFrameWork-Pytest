import pytest
from utils.excel import *
import os
import copy
import datetime
import string

base_dir = os.path.dirname(__file__)

cases = []


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
        # global cases
        # cases = copy.deepcopy(test_data)
        metafunc.parametrize("parameters", test_data, ids=ids, scope="function")  # 用test_data这个列表对parameters进行参数化


# @pytest.hookimpl(hookwrapper=True, tryfirst=True)
# def pytest_runtest_makereport(item, call):
#     print('------------------------------------')
#
#     # 获取钩子方法的调用结果
#     out = yield
#     report = out.get_result()
#     if report.when == "call":
#         logs = "\n".join(["\n".join(section) for section in report.sections])  # 用例执行日志
#         logs = "\n | INFO |".join(logs.split("| INFO |")) # 换行处理
#         result = 1 if report.outcome == 'passed' else 0  # 是否通过
#         duration = report.duration  # 执行时间
#         title = report.nodeid.split("[")[1].rstrip("]")
#         result_info = {
#             "logs": logs,
#             "result": result,
#             "duration": duration,
#         }
#         # 更新结果
#         for case in cases:
#             if case["title"] == title:
#                 case.update(result_info)
#
#
# def generate_report(path='/reports/', **kwargs):
#     with open(base_dir + path + 'template.html', 'r') as f:
#         template_html_str = f.read()
#     filename = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '.html'
#     with open(base_dir + path + filename, 'w') as f:
#         template = string.Template(template_html_str)  # 获取一个模板文件
#         print(kwargs)
#         html_str = template.substitute(kwargs)
#         f.write(html_str)
#
#
# @pytest.fixture(scope="module", autouse=True)
# def setup_fixture():
#     print("所有用例开始执行...")
#     yield
#     print("执行完毕，收集测试结果生成测试报告...")
#     # 结束后生成测试报告
#     for case in cases:
#         for k, v in case.items():
#             if v == None:
#                 case[k] = ""
#
#     success = len(list(filter(lambda x: x["result"] == 1, cases)))
#     failed = len(cases)-success
#     duration = sum([case["duration"] for case in cases])
#     avg_duration = duration/len(cases)
#     summary = {
#         "total": len(cases),
#         "success": success,
#         "failed": failed,
#         "success_rate": success/len(cases),
#         "fail_rate": failed/len(cases),
#         "duration": duration,
#         "avg_duration": avg_duration
#     }
#     series_data = [
#         {"value": success, "name": 'Success'},
#         {"value": failed, "name": 'Failed'}
#     ]
#
#     generate_report(cases=cases, summary=summary, series_data=series_data)
