from django.db import models
from simditor.fields import RichTextField
# Create your models here.

class Project(models.Model):

    class Meta:
        verbose_name = "项目内容"
        verbose_name_plural = "项目内容"

    def __str__(self):
        return self.title
    
    content = RichTextField(verbose_name='项目内容')


class SSZModel(models.Model):

    class Meta:
        verbose_name = "SSZ联赛"
        verbose_name_plural = "SSZ联赛"

    content = RichTextField(verbose_name='项目内容')
    