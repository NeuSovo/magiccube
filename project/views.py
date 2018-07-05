from django.shortcuts import render
from .models import *
from dss.Serializer import serializer
from utils.tools import parse_info
from django.http import Http404
# Create your views here.

def get_project_view(request, project_id = None):
    if project_id:
        try:
            project = Project.objects.get(id=project_id)
        except:
            raise Http404("project_id: {} 错误".format(project_id))
        return parse_info({'info':serializer(project)})

    return parse_info({'lists': serializer(Project.objects.all(), exclude_attr=('content'))})

