from django.db import models
from simditor.fields import RichTextField
# Create your models here.

class Project(models.Model):

    class Meta:
        verbose_name = "添加项目"
        verbose_name_plural = "添加项目"

    def __str__(self):
        return self.title
    
    title = models.CharField(verbose_name='项目名称', max_length=50)
    content = RichTextField(verbose_name='项目介绍')