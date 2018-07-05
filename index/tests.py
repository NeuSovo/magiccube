from django.test import TestCase, Client
from .models import *
# Create your tests here.

class IndexTestCase(TestCase):

    def setUp(self):
        News(title="test", content="test", create_user="1",
             is_top="1", news_url="https://123").save()

    def test_news(self):
        c = Client()
        rep = c.get('/api/index/news/')
        self.assertEqual(rep.status_code, 200)
        self.assertContains(rep, 'news_list')

    def test_events(self):
        c = Client()
        rep = c.get('/api/index/recentevent/')
        self.assertEqual(rep.status_code, 200)

    def test_hotvideo(self):
        c = Client()
        rep = c.get('/api/index/hotvideo/')
        self.assertEqual(rep.status_code, 200)

    def test_join(self):
        c = Client()
        rep = c.get('/api/index/join/')
        self.assertEqual(rep.status_code, 200)

    def test_lunbo(self):
        c = Client()
        rep = c.get('/api/index/lunbo/')
        self.assertEqual(rep.status_code, 200)