import requests


class GetToken:
    # 获取token的接口，属于万年不变的，数据也不用分离了
    appid = 'xxx'  # 登陆公众平台后获取
    secret = 'xxx'

    def get_token(self):
        res = requests.get(
            'https://api.weixin.qq.com/cgi-bin/token',
            params={
                'grant_type': 'client_credential',
                'appid': self.appid,
                'secret': self.secret
            })
        print('get token', res.json())
        return res.json()['access_token']

    def test_token(self, appid, secret):
        """
        测试获取token的业务方法，会在case中调用，此接口没有做业务驱动
        :param appid:
        :param secret:
        :return:
        """
        res = requests.request(
            method='get',
            url='https://api.weixin.qq.com/cgi-bin/token',
            params={
                'grant_type': 'client_credential',
                'appid': appid,
                'secret': secret
            }
        )
        return res


if __name__ == '__main__':
    GetToken().get_token()
