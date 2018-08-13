from rest_framework.pagination import PageNumberPagination
from django.db import models
from utils.models import User, UserProfile
from event.models import Events, EventType, EventTypeDetail


class CommonPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'


class Authority(models.Model):
    TRUN = ((0, '决赛'), (1, '半决赛'), (2, '初赛'), (3, '复赛'), (4, '组合制决赛'), (6, '组合制初赛'),)
    Award = ((0, '否'), (1, '金'), (2, '银'), (3, '铜'))
    username = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    events = models.ForeignKey(Events, on_delete=models.CASCADE, verbose_name='赛事')
    eventType = models.ForeignKey(EventTypeDetail, on_delete=models.CASCADE, related_name='eventType', verbose_name='类型')
    single = models.DecimalField(verbose_name='单次成绩', max_digits=5, decimal_places=2)
    turn = models.SmallIntegerField(verbose_name='轮次', choices=TRUN, default=0)
    recent = models.DateField(verbose_name='参加时间', auto_now_add=True)
    award = models.SmallIntegerField(verbose_name='是否获奖', choices=Award, default=0)

    def username_str(self):
        return self.username.userprofile.username

    def events_str(self):
        return self.events.name

    def eventType_str(self):
        return self.eventType.type.type

    def __str__(self):
        return '{}'.format(self.username)

    class Meta:
        verbose_name_plural = '官方成绩'  # ordering = ('username',)
