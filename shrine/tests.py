from django.test import TestCase
from django.test import Client
from cms.tests import UserTestCase
from cms.models import *
from datetime import datetime


# Create your tests here.
# class EventsTests(TestCase):
#     def setUp(self):
#         self.eventprovince = EventProvince(province='测试省')
#         self.eventprovince.save()
#         self.eventproject = EventProject(project="测试项目")
#         self.eventproject.save()
#         self.eventtype = EventType(type="测试类型")
#         self.eventtype.save()
#         self.event = Events(name="测试赛事", location='无', event_province=self.eventprovince,
#                             event_project=self.eventproject)
#         self.event.save()
#         self.eventtypedetail = EventTypeDetail(type=self.eventtype, lines="1", price="test", event=self.event)
#         self.eventtypedetail.save()
#         self.eventsdetail = EventsDetail(event=self.event, evnet_org="evnet_org", evnet_represent="evnet_represent",
#                                          apply_count=1200, event_apply_begin_time=datetime.now(),
#                                          event_apply_end_time=datetime.now(), event_about="无")
#         self.eventsdetail.save()
#
#         self.eventrules = EventRules(event=self.event)
#         self.eventrules.save()
#         self.eventtraffic = EventTraffic(event=self.event)
#         self.eventtraffic.save()
#         self.eventsc = EventSc(event=self.event)
#         self.eventsc.save()
#         self.event_id = self.event.id
#
#     def test_get_all_event(self):
#         c = Client()
#         rep = c.get('/api/event/?year=2018&type=1&province=1&project=1')
#         self.assertEqual(rep.status_code, 200)
#
#     def test_get_event_all_fliter(self):
#         c = Client()
#         rep = c.get('/api/event/getfilter')
#         self.assertEqual(rep.status_code, 200)
#
#     def test_get_event_detail(self):
#         c = Client()
#         rep = c.get('/api/event/detail/{}'.format(self.event_id))
#         self.assertEqual(rep.status_code, 200)
#
#     def test_get_event_types(self):
#         c = Client()
#         rep = c.get('/api/event/type/{}'.format(self.event_id))
#         self.assertEqual(rep.status_code, 200)
#
#     def test_get_event_types_404(self):
#         c = Client()
#         rep = c.get('/api/event/type/404')
#         self.assertEqual(rep.status_code, 404)
#
#     def test_get_event_rules(self):
#         c = Client()
#         rep = c.get('/api/event/rules/{}'.format(self.event_id))
#         self.assertEqual(rep.status_code, 200)
#
#     def test_get_event_traffic(self):
#         c = Client()
#         rep = c.get('/api/event/traffic/{}'.format(self.event_id))
#         self.assertEqual(rep.status_code, 200)
#
#     def test_get_event_sc(self):
#         c = Client()
#         rep = c.get('/api/event/sc/{}'.format(self.event_id))
#         self.assertEqual(rep.status_code, 200)


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
