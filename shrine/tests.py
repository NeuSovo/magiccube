from django.test import TestCase
from django.test import Client
from utils.models import *
from datetime import datetime


class UserRecodeTest(TestCase):
    def setUp(self):
        profile = {'sex': '男', 'birthday': '1992', 'phone': '123', 'country': '中国', 'province': '河南', 'city': ',',
                   'paperwork_type': '123', 'paperwork_id': '123'}
        self.user = User.reg_user(email='test@qq.com', username='test', password='test')
        self.userprofile = UserProfile.objects.update(username='test', **profile)
        self.c = Client()

    def test_get_user_all(self):
        res = self.c.get('/api/recode/user/')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()['results'],
                         [{'id': 1, 'userprofile': {'username': 'test', 'sex': '男', 'country': '中国'}}])

    def test_authority(self):
        rep = self.c.get('/api/recode/rank/authority/')
        self.assertEqual(rep.status_code, 200)

    def test_rank(self):
        rep = self.c.get('/api/recode/rank/')
        self.assertEqual(rep.status_code, 200)

    def test_contest(self):
        rep = self.c.get('/api/recode/contest/')
        self.assertEqual(rep.status_code, 200)
