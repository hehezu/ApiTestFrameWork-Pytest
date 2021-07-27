# ApiTestFrameWork-Pytest

#### 介绍

ApiTestFrameWork的pytest版本。感兴趣可以看看，基于excel的自动化框架, 供学习使用。

### 项目说明

本框架是为了快速实现http/https协议而设计的一套数据驱动自动化接口框架,基于EXCEL+requests+unittest+ddt设计,pytest作为执行器,本框架无需你使用代码编写用例,那你可能 会担心万一有接口之间相互依赖,或者说需要登入的token等之类的接口,该如何编写用例,在这里告诉你们笨框架已经完美解决此问题,所有的一切将在EXCEL中进行！！本框架实现了在EXCEL中 进行接口用例编写,接口关联,接口断言,还有很重要的一点,实现了类似jmeter函数助手的功能,譬如生成UUID,随机定长字符串,格式化日期,正则表达式等,只需要你在EXCCEL中使用特殊的写法就能够使用这些函数啦~~是不是很期待！！

### 环境安装

1. 从本项目clone到本地
2. 新建虚拟环境
3. pip install -r requirements.txt



#### 技术栈

- requests
- pytest
- pytest-tmreport (本人开发的报告插件)
- openpyxl
- loguru

#### 项目结构说明

1.  cases ================> 测试用例
2.  data =================> 测试数据
3.  reports ==============> 测试报告
4。 utils ================> 工具类
5。 conftest.py ==========> pytest conftest

#### EXCEL字段解析

- title: 用例标题
- url: 接口地址
- method: 请求方式(支持所有)
- headers: 请求头,格式为 {"key","value"}
- cookies: Cookies就是Cookies啦,格式为 {"key":"value"}
- params: 请求参数,注意是参数而不是请求体,类似url后拼接的?key=value&key=value,格式为 {"key":"value"}
- body: 请求体,格式为 {"key":"value"}
- jsonpath_exp_save: JSONPATH提取表达式,格式为 自定义key=JSONPATH表达式 （支持英文分号分割，支持多组）
- regular_exp_save: 正则提取表达式,格式为 自定义key=正则表达式 （支持英文分号分割，支持多组）
- jsonpath_exp_assertion: JSONPATH断言,格式为 JSONPATH=预期结果 （支持英文分号分割，支持多组）
- regular_exp_assertion: 正则断言,格式为 正则表达式=预期结果 （支持英文分号分割，支持多组）


#### 使用方式

1. 在data下的test.xlsx中填写测试数据 (例子可以参考目前test.xlsx的数据)
2. 使用命令行执行 pytest -s cases/test_pytest.py
3. 如果需要生成测试报告，使用 pytest cases/test_pytest.py --pytest-tmreport-name reports/report.html