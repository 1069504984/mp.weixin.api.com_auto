import logging
import allure
import pytest
from api.base_api import BaseApi
from api.get_token import GetToken

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',  # 日志格式
                    datefmt='%Y-%m-%d %H:%M:%S',  # 时间格式：2018-11-12 23:50:21
                    # filename='../logs/test.log',    # 日志的输出路径
                    filemode='a')


@allure.feature('获取token')
class TestToken:
    """
    获取token的用例，这里用了用例的数据驱动
    """
    ba = BaseApi()
    data = ba.yaml_load('../data/test_token.data.yaml')  # 封装的yaml文件加载与读取方法

    @allure.severity('blocker')
    @pytest.mark.flaky(reruns=1, reruns_delay=1)  # 失败重试1次，间隔1秒
    @pytest.mark.parametrize('appid, secret, asserts, expect', data['test_token'])
    def test_token(self, appid, secret, asserts, expect):
        res = GetToken().test_token(appid, secret)  # 调用业务方法，发送请求，拿到request对象
        logging.info(
            '\n 获取token： \n - appid: {} \n - secret: {} \n - asserts: {} \n - expect: {} \n 返回值: {}'.
            format(appid, secret, asserts, expect, res.json())
        )
        self.ba.apple(res, asserts, expect)  # 定制的断言方法，传入：res，断言目标（实际结果），预期结果
