import django_filters
from .models import *


class TestFilter(django_filters.rest_framework.FilterSet):
    min_id = django_filters.NumberFilter(name='id', lookup_expr='gte')
    max_id = django_filters.NumberFilter(name='id', lookup_expr='lte')

    class Meta:
        model = test
        fields = ['title', 'code', 'min_id', 'max_id']
