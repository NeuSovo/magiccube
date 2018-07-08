from django.shortcuts import render

# Create your views here.
from utils.tools import parse_info
from .models import *
def get_join_our(request):
    info = JoinOur.objects.all()[:1]
    if info:
        return parse_info({'info': info[0].info})
    return parse_info({})