from django.db import models
from utils.models import UserProfile
# Create your models here.

class UserParagraph(models.Model):
    class Meta:
        verbose_name = "用户段位认证"
        verbose_name_plural = "用户段位认证"
        ordering = ['username']

    def __str__(self):
        return self.username

    @property
    def username(self):
        return self.username
    
    # userinfo = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="用户")
    username = models.CharField(verbose_name='用户名', max_length=100)
    country = models.CharField(
        max_length=20, null=True, blank=True, verbose_name='地区')
    province = models.CharField(
        max_length=20, null=True, blank=True, verbose_name='省份')
    sex = models.CharField(max_length=20, null=True, blank=True, verbose_name='性别')
    rz_date = models.DateTimeField(auto_now_add=True, verbose_name="认证时间")
    paragraph = models.CharField(max_length=100, verbose_name="段位")
    zs_img = models.ImageField(verbose_name='证书', default='none', upload_to="img")


class RzgParagraph(models.Model):
    class Meta:
        verbose_name = "认证官"
        verbose_name_plural = "认证官"
        ordering = ['name']

    def __str__(self):
        return self.name

    country = models.CharField(max_length=50, verbose_name="地区")
    name = models.CharField(max_length=50, verbose_name="姓名")
    sex = models.CharField(max_length=50, verbose_name="性别")
    phone = models.BigIntegerField(verbose_name="认证编号")
    wechat = models.CharField(max_length=100, verbose_name='微信')
    zs_img = models.ImageField(verbose_name='证书', default='none', upload_to="img")


class JlParagraph(models.Model):
    class Meta:
        verbose_name = "教练证书"
        verbose_name_plural = "教练证书"
        ordering = ['name']

    def __str__(self):
        return self.name

    country = models.CharField(max_length=50, verbose_name="地区")
    name = models.CharField(max_length=50, verbose_name="姓名")
    paragraph = models.CharField(max_length=100, verbose_name="级别")
    zs_img = models.ImageField(verbose_name='证书', default='none', upload_to="img")
    zs_number = models.CharField(max_length=50, verbose_name="证书编号")

