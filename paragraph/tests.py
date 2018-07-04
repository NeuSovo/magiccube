from django.test import TestCase,Client
from .models import *

# Create your tests here.
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