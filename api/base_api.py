import datetime
import json
import random
from jsonpath import jsonpath
import pymysql
import requests
import yaml
from api.get_token import GetToken
import requests_mock
import configparser


class BaseApi:
    params = {}
    _data = {}
    _url = 'https://api.weixin.qq.com'
    # url = 'xxx'
    token = GetToken().get_token()

    @classmethod
    def yaml_load(cls, path):
        # 封装yaml文件的加载
        with open(path, encoding='UTF-8') as f:
            return yaml.safe_load(f)

    @classmethod
    def format(cls, r):
        cls.r = r
        # print(json.dumps(r.json(), indent=2))
        print(json.dumps(json.loads(r.text), indent=2, ensure_ascii=False))

    def jsonpath(self, path, r=None, **kwargs):
        if r is None:
            r = self.r.json()
        return jsonpath(r, path)

    @classmethod
    def apple(cls, res, asserts, expect):
        """
        封装断言
        todo 移动到action
        :param res: 响应数据
        :param asserts: 断言对象
        :param expect: 预期结果
        :return:
        """

        if asserts == 'expires_in':
            assert res.json()['expires_in'] <= expect
        elif asserts == 'errcode':
            assert res.json()['errcode'] == expect

    @classmethod
    def mobile(cls):
        """
        随机生成122开头手机号
        todo 移动到action
        :return:
        """
        mobile = '122' + ''.join(random.choice("0123456789") for i in range(8))
        return mobile

    def api_send(self, req: dict):
        """
        数据驱动的关键，封装了参数替换及请求发送
        :param req: 加载后的yaml文件，在业务方法中传递，
        :return: request实例对象
        """
        # req['headers']['token'] = self.token  # 给token赋值,token在headers中
        req['params']['access_token'] = self.token  # 给token赋值,token在url中
        # 模板内容替换  yaml文件中的变量赋值
        raw = yaml.dump(req)  # 转为字符串
        raw = raw.replace(f'${{url}}', self._url)  # 替换url，便于环境切换

        for key, value in self.params.items():  # 替换参数（测试数据）
            if isinstance(value, datetime.date):
                value = value.strftime('%Y-%m-%d')
                raw = raw.replace(f"${{{key}}}", repr(value))  # 如果参数是datetime.date类型的，先转为字符串
            else:
                raw = raw.replace(f"${{{key}}}", repr(value))
        req = yaml.safe_load(raw)  # 转为yaml
        print('参数', req)

        r = requests.request(
            method=req['method'],
            url=req['url'],
            params=req['params'],
            headers=req['headers'],
            proxies=req['proxies'],  # 代理
            verify=req['verify'],  # 证书
            json=req['json']
        )
        # print(r.json())
        return r

    def steps_run(self, steps: list):

        for step in steps:
            # print(step)
            # 模板内容替换
            # todo: 使用format
            raw = yaml.dump(step)
            for key, value in self.params.items():
                raw = raw.replace(f"${{{key}}}", repr(value))
                # print("replace")
                # print(raw)
            step = yaml.safe_load(raw)

            if isinstance(step, dict):
                if "method" in step.keys():
                    method = step['method'].split('.')[-1]
                    # todo: 用装饰器精简参数
                    getattr(self, method)(**step)  # 调用实例化对象（谁调的这个方法谁就是self，一般是子类下的方法）下的method方法
                if "extract" in step.keys():
                    self._data[step["extract"]] = getattr(self, 'jsonpath')(**step)
                    print("extract")
                    print(self._data[step["extract"]])

                if "assertion" in step.keys():
                    assertion = step["assertion"]
                    if isinstance(assertion, str):
                        assert eval(assertion)
                    if assertion[1] == "eq":
                        assert assertion[0] == assertion[2]

    def mock_response(self, method, url, json):
        """
        mock响应
        todo 优化, 移动到action
        :param method: 请求方法
        :param url: 请求url
        :param json: mock的响应数据
        """
        with requests_mock.Mocker() as m:
            m.request(method=method, url=url, json=json)
            res = requests.request(method=method, url=url)
        return res

    def get_config(self, path, name):
        """
        配置文件读取
        todo 移动到action
        :param path: 路径
        :param name: section名
        :return: 该section下的所有键值对
        """
        cf = configparser.ConfigParser()
        cf.read(path)  # 读取配置文件，如果写文件的绝对路径，就可以不用os模块
        # secs = cf.sections()  # 获取文件中所有的section(一个配置文件中可以有多个配置，如数据库相关的配置，邮箱相关的配置)
        # host = cf.get(name, 'host')  # 获取host
        items = dict(cf.items(name))  # 获取section名为Mysql-Database所对应的全部键值对
        return items

    def connect_db(self, path, name):
        """
        数据库连接
        todo 移动到action
        :param path: 配置文件路径
        :param name: section名
        :return:
        """
        data = self.get_config(path, name)
        try:
            db_connect = pymysql.connect(host=data['host'], user=data['user'], password=data['password'], db=data['db'],
                                         charset=data['charset'])
            return db_connect
        except Exception:
            print('连接失败')
