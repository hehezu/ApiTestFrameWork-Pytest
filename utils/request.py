import requests
import jsonpath
import json
import re
from loguru import logger


class RequestUtil(requests.Session):  # 可以自动缓存Cookie

    def __init__(self):
        super().__init__()
        self.variable_pool = {}  # 全局变量池

    def send_request(self, method, url, title, jsonpath_exp_save=None, regular_exp_save=None,
                     jsonpath_exp_assertion=None, regular_exp_assertion=None, **kwargs):
        """
        发送请求
        需求：1.调接口，get/post/put/delete
            2.需要打印相关日志
            3.异常处理
            4.重试机制
            5.超时...
        :return:
        """
        logger.info(f"CASE {title} START".center(40, "*"))
        logger.info(f"接口请求方式：{method}")
        logger.info(f"接口url：{self.replace_template_str(url)}")
        logger.info(f"JSONPATH提取表达式： {jsonpath_exp_save}")
        logger.info(f"正则提取表达式： {regular_exp_save}")
        logger.info(f"JSONPATH断言表达式： {jsonpath_exp_assertion}")
        logger.info(f"正则断言表达式： {regular_exp_assertion}")
        for k, v in kwargs.items():
            if v is not None:
                try:
                    kwargs[k] = json.loads(self.replace_template_str(v))
                except:
                    logger.error(f"参数({k})格式不正确")
        response = self.request(method, url, **kwargs)  # 调用接口
        response_str = response.text
        try:
            response_str = json.loads(response_str)  # 转成字典
            response_str = json.dumps(response_str, indent=4, ensure_ascii=False)
        except:
            logger.warning("响应JSON转换失败！保持原来格式！")
        logger.info(f"response text: \n {response_str}")
        # 判断是否需要关联参数, 如果有，判断是正则提取还是jsonpath提取，做对应处理，处理多参数情况存储
        if jsonpath_exp_save or regular_exp_save:
            if jsonpath_exp_save:
                json_kv_list = jsonpath_exp_save.split(";")
                for json_kv in json_kv_list:
                    key = json_kv.split("=")[0]
                    jsonpath_str = json_kv.split("=")[1]
                    self.save_variables(response_str, key, jsonpath_str)
            if regular_exp_save:
                regular_kv_list = regular_exp_save.split(";")
                for regular_kv in regular_kv_list:
                    key = regular_kv.split("=")[0]
                    regular_str = regular_kv.split("=")[1]
                    self.save_variables(response_str, key, regular_str)
        # 判断是否有断言，如果有就进行
        if jsonpath_exp_assertion or regular_exp_assertion:
            if jsonpath_exp_assertion:
                json_kv_list = jsonpath_exp_assertion.split(";")
                for json_kv in json_kv_list:
                    jsonpath_str = json_kv.split("=")[0]
                    value = json_kv.split("=")[1]
                    self.assert_by_expression(response_str, value, jsonpath_str)
            if regular_exp_assertion:
                regular_kv_list = regular_exp_assertion.split(";")
                for regular_kv in regular_kv_list:
                    regular_str = regular_kv.split("=")[0]
                    value = regular_kv.split("=")[1]
                    self.assert_by_expression(response_str, value, regular_str)
        logger.info("CASE END".center(40, "*"))
        # 判断是否需要关联
        # 判断是否需要断言

    def save_variables(self, target_str, key, jsonpath_expression=None, regular_expression=None):
        """
        保存关联参数到参数池
        :return:
        """
        target = None
        if isinstance(target_str, str):
            try:
                target = json.loads(target_str)
            except:
                target = target_str
        match_value = jsonpath.jsonpath(target, jsonpath_expression) if jsonpath_expression else re.findall(
            regular_expression)
        if match_value is False or match_value == []:
            logger.error(f"Failed to extract variable （key: {key}）")
            return
        match_value = match_value[0] if match_value else match_value
        self.variable_pool[key] = match_value  # 存储变量到变量池
        logger.info(f"set variable ({key} = {match_value}) to variable pool")
        logger.info(f"global variable pool: {self.variable_pool} ")

    def replace_template_str(self, target_str):
        """
        替换{{key}}位全局变量池的参数
        :return:
        """
        match_values = re.findall("\{\{(.*?)\}\}", target_str)
        if not match_values:
            logger.info(f"Target_Str: {target_str}, This is no variable to be replaced")
            return target_str
        logger.info(f"The variable to be replaced is ({match_values})")
        for key in match_values:
            value = self.variable_pool.get(key)
            replace_str = "{{" + key + "}}"
            target_str = target_str.replace(replace_str, str(value))
            logger.info(f"replace {replace_str} to {value}")
        return target_str

    def assert_by_expression(self, target_str, value, jsonpath_expression=None, regular_expression=None):
        """
        断言
        :param target_str:
        :param value:
        :param jsonpath_expression:
        :param regular_expression:
        :return:
        """

        target = None
        if isinstance(target_str, str):
            target = json.loads(target_str)
        match_value = jsonpath.jsonpath(target, jsonpath_expression) if jsonpath_expression else re.findall(
            regular_expression)
        if match_value is False or match_value == []:
            logger.error(f"Failed to extract variable （key: {key}）")
            return
        match_value = match_value[0] if match_value else match_value  # 匹配到实际的值
        try:
            assert str(match_value) == str(value)
            logger.info(f"断言成功! {match_value} == {value}")
        except AssertionError:
            logger.error(f"断言失败! {match_value} != {value}")
            raise AssertionError(f"断言失败! {match_value} != {value}")