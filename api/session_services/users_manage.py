from api.base_api import BaseApi


class UsersManage(BaseApi):
    """
    用户管理接口集,
    首先明确需要接收哪些参数，即测试用例的元素
    """
    data = BaseApi.yaml_load('../data/users_manage.api.yaml')

    def create_tags(self, name):
        """
        创建标签接口，实现业务的数据驱动
        :param name: 标签名
        :return: 实例request对象
        """
        self.params = {'name': name}  # 为了完成参数替换
        res = self.api_send(self.data['create_tags'])  # 业务的数据驱动
        return res

    def get_tags(self):
        """
        获取标签接口，get请求，没有参数
        :return:
        """
        return self.api_send(self.data['get_tags'])

    def delete_tags(self, id):
        """
        删除标签接口，post请求
        :param id: 标签id
        :return:
        """
        self.params = {'id': id}
        res = self.api_send(self.data['delete_tags'])
        return res

    def get_db_tags(self):
        """
        从数据库中拿标签，sql语句可以优化到配置文件中
        :return:
        """
        db_connect = self.connect_db('config.ini', 'MySQL-Database')  # 连接数据取
        cursor = db_connect.cursor()  # 获取游标
        sql = """CREATE TABLE Tags (
                 id int(20) NOT NULL AUTO_INCREMENT COMMENT '主键id',
                 name varchar(255),
                 PRIMARY KEY(id)
                 )ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;"""
        cursor.execute("DROP TABLE IF EXISTS Tags")  # 如果有就删除
        cursor.execute(sql)  # 执行创建表语句
        cursor.execute(
            "INSERT INTO Tags(Tags.name) VALUES ('星标组'), ('青铜'), ('白银'), ('黄金'), ('白金')")  # 插入数据
        db_connect.commit()  # 提交插入动作到数据库
        try:
            cursor.execute('select name from Tags WHERE id = 1')  # 执行查询语句
            res = list(cursor.fetchall())  # 获取所有语句
            return res[0][0]
        except Exception:
            print('查询失败')
        db_connect.close()  # 关闭连接