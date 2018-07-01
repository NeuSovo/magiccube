from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(test)
admin.site.register(test0)


@admin.register(test1)
class test1Admin(admin.ModelAdmin):
    list_display = ['title', 'list', 'str']


@admin.register(Authority)
class AuthorityAdmin(admin.ModelAdmin):
    # 显示字段
    list_display = ['id', 'username', 'turn', 'single', 'average']

    # 能更改的字段  # fields = ['username', 'events']  # def username(self, obj):  #     return obj.username.username
