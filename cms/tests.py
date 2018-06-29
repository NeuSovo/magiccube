from django.test import TestCase, Client
from django.test import Client
from .views import *
from .models import *
from datetime import datetime
# Create your tests here.


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


class EventsTests(TestCase):
    def setUp(self):
        self.eventprovince = EventProvince(province='测试省')
        self.eventprovince.save()
        self.eventproject = EventProject(project="测试项目")
        self.eventproject.save()
        self.eventtype = EventType(type="测试类型")
        self.eventtype.save()
        self.event = Events(name="测试赛事", location='无',
                            event_province=self.eventprovince, event_project=self.eventproject)
        self.event.save()
        self.eventtypedetail = EventTypeDetail(
            type=self.eventtype, lines="1", price="test", event=self.event)
        self.eventtypedetail.save()
        self.eventsdetail = EventsDetail(event=self.event, evnet_org="evnet_org",
                                         evnet_represent="evnet_represent", apply_count=1200, 
                                         event_apply_begin_time=datetime.now(), 
                                         event_apply_end_time=datetime.now(), event_about="无")
        self.eventsdetail.save()

        self.eventrules = EventRules(event=self.event)
        self.eventrules.save()
        self.eventtraffic = EventTraffic(event=self.event)
        self.eventtraffic.save()
        self.eventsc = EventSc(event=self.event)
        self.eventsc.save()
        self.event_id = self.event.id

    def test_get_all_event(self):
        c = Client()
        rep = c.get('/api/event/?year=2018&type=1&province=1&project=1')
        self.assertEqual(rep.status_code, 200)


    def test_get_event_all_fliter(self):
        c = Client()
        rep = c.get('/api/event/getfilter')
        self.assertEqual(rep.status_code, 200)

    def test_get_event_detail(self):
        c = Client()
        rep = c.get('/api/event/detail/{}'.format(self.event_id))
        self.assertEqual(rep.status_code, 200)

    def test_get_event_types(self):
        c = Client()
        rep = c.get('/api/event/type/{}'.format(self.event_id))
        self.assertEqual(rep.status_code, 200)

    def test_get_event_types_404(self):
        c = Client()
        rep = c.get('/api/event/type/404')
        self.assertEqual(rep.status_code, 404)

    def test_get_event_rules(self):
        c = Client()
        rep = c.get('/api/event/rules/{}'.format(self.event_id))
        self.assertEqual(rep.status_code, 200)

    def test_get_event_traffic(self):
        c = Client()
        rep = c.get('/api/event/traffic/{}'.format(self.event_id))
        self.assertEqual(rep.status_code, 200)

    def test_get_event_sc(self):
        c = Client()
        rep = c.get('/api/event/sc/{}'.format(self.event_id))
        self.assertEqual(rep.status_code, 200)


class ApplyTestCase(TestCase):
    def setUp(self):
        self.eventprovince = EventProvince(province='测试省')
        self.eventprovince.save()
        self.eventproject = EventProject(project="测试项目")
        self.eventproject.save()
        self.eventtype = EventType(type="测试类型")
        self.eventtype.save()
        self.event = Events(name="测试赛事", location='无',
                            event_province=self.eventprovince, event_project=self.eventproject)
        self.event.save()
        self.eventtypedetail = EventTypeDetail(
            type=self.eventtype, lines="1", price="test", event=self.event)
        self.eventtypedetail.save()
        self.eventsdetail = EventsDetail(event=self.event, evnet_org="evnet_org",
                                         evnet_represent="evnet_represent", apply_count=1200, 
                                         event_apply_begin_time=datetime.now(), 
                                         event_apply_end_time=datetime.now(), event_about="无")
        self.eventsdetail.save()

        self.eventrules = EventRules(event=self.event)
        self.eventrules.save()
        self.eventtraffic = EventTraffic(event=self.event)
        self.eventtraffic.save()
        self.eventsc = EventSc(event=self.event)
        self.eventsc.save()
        self.event_id = self.event.id
        self.events_type_id = self.eventtypedetail.id


        self.user = User.reg_user(
            email='test@qq.com', username='test', password='test')
        self.c = Client()
        res = self.c.post('/api/auth/login',
                    {'email': 'test@qq.com', 'password': 'test'})
        self.token = res.json()['access_token']


    def test_apply(self):
        data = {
            'event_id': self.event_id,
            'total_price': 122,
            'remarks': '无',
            'types': self.events_type_id
        }

        rep = self.c.post('/api/event/apply', data)
        self.assertEqual(rep.status_code, 200)
        self.assertContains(rep, 'apply_id')

        # re apply
        rep = self.c.post('/api/event/apply', data)
        self.assertEqual(rep.status_code, 200)
        self.assertContains(rep, 'msg')

    def test_get_user_apply(self):
        rep = self.c.get('/api/user/getapply')
        self.assertEqual(rep.status_code, 200)

    def test_invalid_cookies(self):
        c = Client()
        rep = c.get('/api/user/getapply')
        self.assertEqual(rep.status_code, 200)

    def test_get_event_user(self):
        c = Client()
        rep = c.get('/api/event/applyuser/{}'.format(self.event_id))
        self.assertEqual(rep.status_code, 200)

    def test_get_event_user_404(self):
        c = Client()
        rep = c.get('/api/event/applyuser/404')
        self.assertEqual(rep.status_code, 404)


class ParagraphTestCase(TestCase):

    def test_user_paragraph(self):
        c = Client()
        rep = c.get('/api/paragraph/user/')
        self.assertEqual(rep.status_code, 200)

    def test_rzg_paragraph(self):
        c = Client()
        rep = c.get('/api/paragraph/rzg/')
        self.assertEqual(rep.status_code, 200)

    def test_rzg_paragraph(self):
        c = Client()
        rep = c.get('/api/paragraph/jl/')
        self.assertEqual(rep.status_code, 200)