from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles

from cms.models import *

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())


# Create your models here.
class test(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()
    linenos = models.BooleanField(default=False)
    language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
    style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('created',)


class test1(models.Model):
    title = models.ForeignKey(test, on_delete=models.CASCADE)
    str = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name_plural = '实验外键'


class Authority(models.Model):
    TRUN = (
        (0, '决赛'),
        (1, '半决赛'),
        (2, '初赛'),
        (3, '复赛'),
        (4, '组合制决赛'),
        (6, '组合制初赛'),
    )

    username = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    events = models.ForeignKey(Events, on_delete=models.CASCADE)
    eventType = models.ForeignKey(EventType, on_delete=models.CASCADE)
    # single=models.DecimalField(verbose_name='单次',max_digits=5,decimal_places=2)
    single = models.TimeField(verbose_name='单次', default='0')
    average = models.TimeField(verbose_name='平均', default='0')
    detail = models.CharField(verbose_name='详情', max_length=50, blank=True)
    turn = models.SmallIntegerField(verbose_name='轮次', choices=TRUN, default=0)

    class Meta:
        verbose_name_plural = '官方记录'
        ordering = ('username',)
