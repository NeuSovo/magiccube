from django.test import TestCase, Client
from .models import *

class ProjectTestCase(TestCase):

    def setUp(self):
        p = Project(title="test", content="test")
        p.save()
        self.id = p.id

    def test_(self):
        c = Client()
        rep = c.get('/api/project/')
        self.assertEqual(rep.status_code, 200)

    def test_p(self):
        c = Client()
        rep = c.get('/api/project/{}/'.format(self.id))
        self.assertEqual(rep.status_code, 200)