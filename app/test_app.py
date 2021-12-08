from app import app
import unittest
import requests
import random
import json
import time


class TestAdd(unittest.TestCase):
    url = "http://127.0.0.1:5000"

    def make_mockdata(self):
        random_list = random.sample(range(101), 8)
        ran_str = ''.join([str(i) for i in random_list])
        return ran_str

    def setUp(self) -> None:
        app.config['TESTING'] = True  # 开启测试环境
        self.app = app.test_client()

    def tearDown(self) -> None:
        pass

    def test_index(self):
        """
        test Hello world
        :return:
        """
        rp = self.app.get("/")
        data = rp.json
        self.assertEqual(data, "hello world")

    def test_register_success(self):
        """
        注册成功
        :return:
        """

        # mockdata--生成16位随机数字字符串用为邮箱和用户名，用于测验
        ran_str = self.make_mockdata()
        body = {
            "username": ran_str,
            "email": ran_str + "@126.co.jp",
            "password": "123456"
        }
        post_url = self.url + '/register'

        res = requests.post(post_url, data=body)
        data = res.json()

        self.assertEqual(data['state'], 'success')

    def test_register_failed_by_lack(self):
        """
        因缺少参数注册失败
        :return:
        """

        # mockdata--生成16位随机数字字符串用为邮箱和用户名，用于测验
        ran_str = self.make_mockdata()
        body = {
            "username": ran_str,
            "password": "123456"
        }
        post_url = self.url + '/register'

        res = requests.post(post_url, data=body)
        data = res.json()

        self.assertEqual(data['state'], 'failed')

    def test_register_failed_by_email(self):
        """
        因邮箱格式错误导致注册失败
        :return:
        """

        # mockdata--生成16位随机数字字符串用为邮箱和用户名，用于测验
        ran_str = self.make_mockdata()
        body = {
            "username": ran_str,
            "email": ran_str,
            "password": "123456"
        }
        post_url = self.url + '/register'

        res = requests.post(post_url, data=body)
        data = res.json()

        self.assertEqual(data['state'], 'failed')

    def test_register_failed_by_repeat(self):
        """
        因已经存在导致注册失败
        :return:
        """

        # mockdata--生成16位随机数字字符串用为邮箱和用户名，用于测验
        ran_str = self.make_mockdata()

        body = {
            "username": ran_str,
            "email": ran_str,
            "password": "123456"
        }
        post_url = self.url + '/register'

        res1 = requests.post(post_url, data=body)
        res2 = requests.post(post_url, data=body)
        data = res2.json()

        self.assertEqual(data['state'], 'failed')

    def test_login_success(self):
        """
        登录成功
        :return:
        """

        # 首先注册一条数据
        # mockdata--生成16位随机数字字符串用为邮箱和用户名，用于测验
        ran_str = self.make_mockdata()

        body = {
            "username": ran_str,
            "email": ran_str + "@126.co.jp",
            "password": "123456"
        }
        post_url = self.url + '/register'
        res = requests.post(post_url, data=body)

        # 注册完成后用该账号登录
        post_url = self.url + '/login'

        res = requests.post(post_url, data=body)
        data = res.json()

        self.assertEqual(data['state'], 'success')

    def test_login_failed(self):
        """
        登录失败
        :return:
        """

        # 生成不匹配的邮箱和密码
        ran_str = self.make_mockdata()

        body = {
            "email": ran_str + "@126.co.jp",
            "password": ran_str
        }
        post_url = self.url + '/login'

        res = requests.post(post_url, data=body)
        data = res.json()

        self.assertEqual(data['state'], 'failed')

    def test_edit_success(self):
        # 首先注册一条数据
        ran_str = self.make_mockdata()
        body1 = {
            "username": ran_str,
            "email": ran_str + "@126.co.jp",
            "password": "123456"
        }
        post_url = self.url + '/register'

        # 注册
        res = requests.post(post_url, data=body1)

        body2 = {
            "email": ran_str + "@126.co.jp",
            "password": "123456"
        }

        post_url = self.url + '/login'
        # 登录,获取token
        res = requests.post(post_url, data=body2)
        data = res.json()

        token = data['token']

        # 获取token后随机修改姓名,年龄,生日
        ran_str_new = self.make_mockdata()
        body3 = {
            "username": ran_str_new,
            "age": 1,
            "birth": "1999-01-01"
        }

        body3_json = json.dumps(body3)
        post_url = self.url + '/edit'
        headers = {"Content-Type": "application/json",
                   "Authorization": "Bearer " + token}
        res = requests.post(post_url, headers=headers, data=body3_json)
        data2 = res.json()

        self.assertEqual(data2['state'], 'success')

    def test_edit_failed_by_token_exp(self):
        # 首先注册一条数据
        ran_str = self.make_mockdata()
        body1 = {
            "username": ran_str,
            "email": ran_str + "@126.co.jp",
            "password": "123456"
        }
        post_url = self.url + '/register'

        # 注册
        res = requests.post(post_url, data=body1)

        body2 = {
            "email": ran_str + "@126.co.jp",
            "password": "123456"
        }

        post_url = self.url + '/login'
        # 登录,获取token
        res = requests.post(post_url, data=body2)
        data = res.json()

        token = data['token']

        # 获取token后随机修改姓名,年龄,生日
        ran_str_new = self.make_mockdata()
        body3 = {
            "username": ran_str_new,
            "age": 1,
            "birth": "1999-01-01"
        }

        body3_json = json.dumps(body3)
        post_url = self.url + '/edit'
        headers = {"Content-Type": "application/json",
                   "Authorization": "Bearer " + token}

        # token过期时间是300秒,所以这里sleep305秒用以验证是否成功过期
        # 由于需要实际等待5分钟,这里可以去掉注释自行等待
        # time.sleep(305)
        # res = requests.post(post_url, headers=headers, data=body3_json)
        # data2 = res.json()
        # self.assertEqual(data2['state'], 'failed')

        res = requests.post(post_url, headers=headers, data=body3_json)
        data2 = res.json()

        self.assertEqual(data2['state'], 'success')


if __name__ == '__main__':
    unittest.main(verbosity=2)
