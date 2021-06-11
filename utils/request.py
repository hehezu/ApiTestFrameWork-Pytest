import requests
from loguru import logger
import time
import jsonpath
import re
import json


class RequestUtil(requests.Session):

    def __init__(self):
        super().__init__()
        self.variable_pool = {}  # 定义变量池
        self.retry_num = 0  # 定义初始次数

    def send_request(self, method, url, desc, jsonpath_exp=None, regular_exp=None, **kwargs):
        logger.info("case start".center(40, "*"))
        logger.info(f"描述：{desc}")
        logger.info(f"接口请求方式：{method}")
        logger.info(f"接口url：{self.replace_template_str(url)}")
        logger.info(f"JSONPATH提取表达式： {jsonpath_exp}")
        logger.info(f"正则提取表达式： {regular_exp}")

        before_time = time.time()
        for k, v in kwargs.items():
            kwargs[k] = self.replace_template_str(v)
            logger.info(f"{k}：{v}")
        logger.info("开始发送请求...")
        response = super().request(method, url, **kwargs)
        after_time = time.time()
        if response.status_code == 200:
            logger.info(f"接口请求完毕，响应：{response.text}, 时间: {after_time - before_time} s")
            logger.info(f"响应cookie: {response.cookies}, 已保存")
        else:
            if self.retry_num > 2:
                self.retry_num = 0
                logger.info("接口请求失败，重试完毕！")
                return response
            logger.info(f"接口请求失败，响应code为 {response.status_code}, 进行第 {self.retry_num + 1} 次重试")
            self.retry_num += 1
            self.send_request(method, url, **kwargs)
        if jsonpath_exp:
            for item in jsonpath_exp.split(";"):
                kvs = item.split("=")
                key = kvs[0]  # 获取关键字
                value = kvs[1]  # 获取jsonpath
                self.save_variable(response.text, key, jsonpath_expression=value)  # 进行JSONPATH提取并保存
        if regular_exp:
            for item in regular_exp.split(";"):
                kvs = item.split("=")
                key = kvs[0]  # 获取关键字
                value = kvs[1]  # 获取正则表达式
                self.save_variable(response.text, key, regular_expression=value)  # 进行正则提取并保存

        logger.info("case end".center(40, "*"))
        return response

    def replace_template_str(self, target):
        # 正则匹配所有{{key}}，并做处理
        EXPR = "\{\{(.*?)\}\}"
        keys = re.findall(EXPR, str(target))
        if keys:
            logger.info(f"变量池中匹配到需替换的参数: {keys}")
        for key in keys:
            value = self.variable_pool.get(key)
            if not value:
                logger.warning("变量池中未匹配到关联参数！不进行替换操作")
                continue
            target = target.replace('{{' + key + '}}', str(value))
            logger.info("替换了{{" + key + "}} 为" + str(value))
        return target

    def save_variable(self, target, key, jsonpath_expression=None, regular_expression=None):
        """
        存储变量到变量池
        :param target: 目标字符串
        :param key: 关键字
        :param jsonpath_expression: JSONPATH表达式
        :param regular_expression: 正则表达式
        :return:
        """
        match_values = jsonpath.jsonpath(json.loads(target), jsonpath_expression) if jsonpath_expression else re.findall(
            regular_expression, target)
        if match_values:
            value = match_values[0]
            self.variable_pool[key] = value
            logger.info(f"保存了变量 {key}（{value}） 到 变量池, 当前变量池参数 {str(self.variable_pool)}")
            return value
        else:
            logger.warning("未匹配到任何参数，不进行保存！")
            return


if __name__ == '__main__':
    request_util = RequestUtil()
    body = {
        "password": "123456",
        "userName": "admin"
    }

    request_util.send_request("post", "http://39.105.34.24:8080/apis/login", desc="登入账户", json=body)
    body = {
        "isTiming": 0,
        "taskName": "test1",
        "taskDesc": "测试1",
        "isParallel": 0,
        "testSets": "[]",
        "times": 3,
        "isDing": 0,
        "dingId": ""
    }
    # headers = {
    #     "Cookie": "JSESSIONID=" + jsession_id
    # }
    request_util.send_request("post", "http://39.105.34.24:8080/apis/task/", desc="新增普通任务", json=body)  # 新增普通任务

    params = {
        "taskName": "",
        "isParallel": ""
    }
    response = request_util.send_request("get", "http://39.105.34.24:8080/apis/task/1", desc="查询普通任务,并保存taskId",
                                         jsonpath_exp="taskId=$.data.list[0].taskId", params=params)
    response = request_util.send_request("delete", "http://39.105.34.24:8080/apis/task/{{taskId}}", desc="根据task_id "
                                                                                                         "删除普通任务")
