from django.shortcuts import render
from .models import *
from dss.Serializer import serializer
from utils.tools import parse_info
from django.http import Http404
# Create your views here.

def get_project_view(request):
    return parse_info({'info': serializer(Project.objects.all()[:1])})


def get_ssz_view(request):
    return parse_info({'info': serializer(SSZModel.objects.all()[:1])})
