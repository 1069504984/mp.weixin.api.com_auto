import logging

import allure
import pytest
from jsonpath import jsonpath

from api.session_services.users_manage import UsersManage

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',  # 日志格式
                    datefmt='%Y-%m-%d %H:%M:%S',  # 时间格式：2018-11-12 23:50:21
                    # filename='../report/log/user_manage.log',  # 日志的输出路径
                    filemode='a')


@allure.feature('用户管理')
class TestUsersManage:
    um = UsersManage()
    data = um.yaml_load('../data/users_manage.data.yaml')

    @allure.severity('blocker')
    @allure.story('删除标签')
    @pytest.mark.parametrize('name', data['test_delete_tags'])
    def test_delete_tags(self, name):
        """
        删除标签：
            获取标签，存在则删除
            增加标签，获取标签数量 x
            删除标签，获取标签数量 y
            断言 x = y+1
        """
        r = self.um.get_tags().json()  # 获取标签
        x = jsonpath(r, f"$.tags[*].name")
        if name in x:
            for i in r['tags']:
                if name in i['name']:
                    self.um.delete_tags(i['id'])  # 如果有就删除

        res = self.um.create_tags(name)  # 新增标签
        num1: int = len(jsonpath(self.um.get_tags().json(), f"$.tags[*].name"))  # 获取标签数量

        self.um.delete_tags(res.json()['tag']['id'])  # 删除标签
        num2: int = len(jsonpath(self.um.get_tags().json(), f"$.tags[*].name"))  # 获取标签数量

        assert num1 == num2 + 1  # 断言
        
    @allure.severity('blocker')
    @allure.story('删除标签')
    @pytest.mark.parametrize('name', data['test_delete_tags'])
    def test_delete_tags_step(self, name):
        """
        删除标签，过程驱动
        :param name: 
        :return: 
        """
        self.tag.params = {"name": name}
        self.um.steps_run(self.steps['test_delete_tags'])

    @allure.severity('critical')
    @allure.story('获取标签')
    def test_get_tags(self):
        """
        获取标签,数据区操作
        """
        res = self.um.get_tags()
        asserts = self.um.get_db_tags()
        logging.info('\n 查询标签：\n 返回值: {}'.format(res.json()))
        assert res.json()['tags'][0]['name'] == asserts
