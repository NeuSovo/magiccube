from django.db import models
from simditor.fields import RichTextField
# Create your models here.


class JoinOur(models.Model):

    class Meta:
        verbose_name = "加盟信息"
        verbose_name_plural = "加盟信息"
        ordering = ['-id']

    def __str__(self):
        return '加盟信息填写, 只会显示最新的'

    info = RichTextField(verbose_name='加盟信息填写')