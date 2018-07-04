from django.test import TestCase, Client

# Create your tests here.
from .models import *
class UserTestCase(TestCase):

    def setUp(self):
        self.user = User.reg_user(
            email='test@qq.com', username='test', password='test')

    def test_reg_user(self):
        c = Client()
        rep = c.post(
            '/api/auth/reg', {'email': 'test2@qq.com', 'username': 'test', 'password': 'test'})
        self.assertEqual(rep.status_code, 200)
        self.assertEqual(rep.json()['user_obj']['email'], 'test2@qq.com')

    def test_login_user(self):
        c = Client()
        rep = c.post('/api/auth/login',
                     {'email': 'test@qq.com', 'password': 'test'})
        self.assertEqual(rep.status_code, 200)
        self.assertContains(rep, 'profile')

    def test_login_invalid_user(self):
        c = Client()
        rep = c.post('/api/auth/login',
                     {'email': 'test@qq.com', 'invalidpassword': 'test'})
        self.assertEqual(rep.status_code, 200)
        self.assertContains(rep, 'msg')

    def test_re_reg(self):
        c = Client()
        rep = c.post(
            '/api/auth/reg', {'email': 'test@qq.com', 'username': 'test', 'password': 'test'})
        self.assertEqual(rep.status_code, 200)
        self.assertContains(rep, 'msg')


class UserProfileTestCase(TestCase):
    def setUp(self):
        self.user = User.reg_user(
            email='test@qq.com', username='test', password='test')
        self.c = Client()
        res = self.c.post('/api/auth/login',
                    {'email': 'test@qq.com', 'password': 'test'})
        self.token = res.json()['access_token']

    def test_update_user_profile(self):
        profile = {
            'username': 'username',
            'sex': '男',
            'birthday': '1992',
            'phone': '123',
            'country': '中国',
            'province': '河南',
            'city': ',',
            'paperwork_type': '123',
            'paperwork_id': '123'
        }
        rep = self.c.post('/api/user/profile', profile)
        rep2 = self.c.get('/api/user/profile')
        self.assertEqual(rep.status_code, 200)
        self.assertEqual(rep.json()['username'], profile['username'])
        self.assertEqual(rep.json()['username'], profile['username'])

    def test_check_email(self):
        c = Client()
        rep = c.get('/api/auth/checkemail?token={}'.format(self.token))
        self.assertEqual(rep.status_code, 200)
        self.assertEqual(rep.json()['msg'], 'success')

    def test_check_invalid_email(self):
        c = Client()
        rep = c.get('/api/auth/checkemail?token={}'.format("invalid token"))
        self.assertEqual(rep.status_code, 200)
        self.assertContains(rep, 'msg')