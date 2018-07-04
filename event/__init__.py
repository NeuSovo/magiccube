import os
from django.apps import AppConfig

default_app_config = 'event.EventConfig'

def get_current_app_name(_file):
    return os.path.split(os.path.dirname(_file))[-1]


class EventConfig(AppConfig):
    name = get_current_app_name(__file__)
    verbose_name=u'赛事'
