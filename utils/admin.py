from django.contrib.auth.hashers import make_password
from django.contrib import admin
from .models import *
# Register your models here.

class UserProfileAdmin(admin.StackedInline):
    model = UserProfile
    can_delete = False

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'username')
    inlines = [
        UserProfileAdmin,
    ]
    # readonly_fields = ('password',)

    def save_model(self, request, obj, form, change):
        password = request.POST['password']
        password = make_password(password)
        obj.password = password
        obj.save()