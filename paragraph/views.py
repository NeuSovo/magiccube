from dss.Mixin import MultipleJsonResponseMixin
from django.views.generic import ListView
# Create your views here.
from django.db.models import Q
from .models import *

class UserParagraphView(MultipleJsonResponseMixin, ListView):
    model = UserParagraph
    paginate_by = 15
    datetime_type = 'string'

    exclude_attr = ('user', 'userinfo_id', 'password','is_email_check', 'reg_date', 'rz_date', 'email', 'phone', 'paperwork_type', 'paperwork_id')


    def get_queryset(self):
        search = self.request.GET.get('search', None)
        queryset = super(UserParagraphView, self).get_queryset()
        if search:
            queryset = queryset.filter(Q(paragraph__contains=search) | Q(username__contains=search) | Q(country__contains=search))

        return queryset


class RzgParagraphView(MultipleJsonResponseMixin, ListView):
    model = RzgParagraph
    paginate_by = 15
    datetime_type = 'string'

    def get_queryset(self):
        search = self.request.GET.get('search', None)
        queryset = super(RzgParagraphView, self).get_queryset()
        if search:
            queryset = queryset.filter(Q(country__contains=search) | Q(name__contains=search))

        return queryset


class JlParagraphView(MultipleJsonResponseMixin, ListView):
    model = JlParagraph
    paginate_by = 15
    datetime_type = 'string'

    def get_queryset(self):
        search = self.request.GET.get('search', None)
        queryset = super(JlParagraphView, self).get_queryset()
        if search:
            queryset = queryset.filter(Q(country__contains=search) | Q(name__contains=search) | Q(paragraph__contains=search))

        return queryset