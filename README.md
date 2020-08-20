# python接口自动化测试框架
本人在学习了霍格沃兹测试学院课程之后，成功将接口自动化落地在工作中，现结合微信公众平台，简单地将代码核心记录下来。
## 简单介绍
环境Windows、python3.x、pytest、requests、allure2

接口文档：https://developers.weixin.qq.com/doc/offiaccount/Basic_Information/Get_access_token.html

各模块简单介绍：

    action：封装公共功能
    api：存放业务方法
    data：存放数据驱动文件，yaml格式
    report：存放测试报告及日志
    testcase：用例
    run：执行用例集并生成报告
## 数据驱动
个人觉得数据驱动是个难点，所以就由浅入深，分别写了三个接口：
test_get_token.py::test_token、
users_manage.py::test_delete_tags、
users_manage.py::test_delete_tags_step，分别对应：
* 1、用例驱动，,通过@pytest.mark.parametrize()调用，yaml文件如下
```yaml
test_token:  # 获取token
  - # 正向流程
    - wx422b3fb558
    - 57ca66df4e85bf7a7cd5827
    - expires_in
    - 7200
  - # appid为空
    - ''
    - 57ca66df4e85bf7a7cd2027
    - errcode
    - 41002
```
* 2、 业务驱动，自己封装调用方法，yaml文件如下
```yaml
headers: &headers
  Content-Type: application/json;charset=utf8

create_tags:  # 创建标签
  method: post
  url: ${url}/cgi-bin/tags/create
  params:
    access_token: ${token}
  headers:
    *headers
  proxies:
  verify:
  json:
    tag:
      name: ${name}
```
* 3、过程驱动，自己封装调用方法，yaml文件如下。（相对来说数据较死板，重构不易，可酌情使用）
```yaml
test_delete:
  - {method: tag.get}
  - {extract: "$..tag[?(@.name=='{name}')]", name: x}
  - {method: tag.delete, conditions: xx}
  - {method: tag.get }
  - {extract: path1, name: size_before}
  - {method: tag.add}
  - {method: tag.get}
  - {extract: path3, name: size_after}
  - {assertion: size_after==size_before}
```
数据驱动的代码写在了base_api.py中。

发邮件、数据库操作、allure报告及装饰器、并发执行、失败重试、mock数据、加解密、环境切换等，代码里几个接口也有体现。

代码更新中。。。 2020.08.14
