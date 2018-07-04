import os
from django.apps import AppConfig

default_app_config = 'paragraph.ParagraphConfig'

def get_current_app_name(_file):
    return os.path.split(os.path.dirname(_file))[-1]


class ParagraphConfig(AppConfig):
    name = get_current_app_name(__file__)
    verbose_name = u'段位认证'
