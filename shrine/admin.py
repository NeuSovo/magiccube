from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(test)


@admin.register(test0)
class test0Admin(admin.ModelAdmin):
    list_display = ['lists', 'str']


@admin.register(test00)
class test00Admin(admin.ModelAdmin):
    list_display = ['lists', 'str']


@admin.register(test000)
class test000Admin(admin.ModelAdmin):
    list_display = ['lists', 'str']


@admin.register(test1)
class test1Admin(admin.ModelAdmin):
    # todo 多对多字段不支持显示 大概是不知道显示那个吧
    list_display = ['title', 'list', 'list00', 'get_many', 'str']


@admin.register(Authority)
class AuthorityAdmin(admin.ModelAdmin):
    # 显示字段
    list_display = ['id', 'username', 'turn', 'single', 'average']

    def username(self, obj):
        return "-".join([obj.usernamex.username])

    username.short_description = '用户'

    # 能更改的字段  # fields = ['username', 'events']  # def username(self, obj):  #     return obj.username.username
