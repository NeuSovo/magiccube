from django.contrib import admin
from django.contrib.auth.hashers import make_password

from .models import *


class UserProfileAdmin(admin.StackedInline):
    model = UserProfile
    can_delete = False


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id','email', 'username')
    inlines = [
        UserProfileAdmin,
    ]
    # readonly_fields = ('password',)

    def save_model(self, request, obj, form, change):
        password = request.POST['password'][0]
        password = make_password(password)
        obj.password = password
        obj.save()


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    '''
        Admin View for News
    '''
    list_display = ('title','create_user', 'create_time','is_top')
    list_filter = ('is_top',)
    # inlines = [
    #     Inline,
    # ]
    # raw_id_fields = ('',)
    readonly_fields = ('create_user', 'create_time')
    # search_fields = ('',)
    list_editable = ('is_top',)

    def save_model(self, request, obj, form, change):
        """
        Given a model instance save it to the database.
        """
        obj.create_user = request.user.username
        obj.save()



class EventsRulesAdmin(admin.StackedInline):
    model = EventRules

class EventsTrafficAdmin(admin.StackedInline):
    model = EventTraffic

class EventsScAdmin(admin.StackedInline):
    model = EventSc

class EventsDetailAdmin(admin.StackedInline):
    model = EventsDetail

class EventsTypeAdmin(admin.TabularInline):
    model = EventTypeDetail


@admin.register(Events)
class EventsAdmin(admin.ModelAdmin):
    '''
        Admin View for Events
    '''
    list_display = ('event_date', 'name', 'location', 'evnet_weight', 'event_province', 'event_project')
    list_filter = ('evnet_weight',)
    inlines = [
        EventsTypeAdmin,
        EventsDetailAdmin,
        EventsRulesAdmin,
        EventsTrafficAdmin,
        EventsScAdmin,
    ]
    # raw_id_fields = ('',)
    # readonly_fields = ('',)
    # search_fields = ('',)

class AppplyUserTypesAdmin(admin.TabularInline):
    model = ApplyUserTypes

@admin.register(ApplyUser)
class ApplyUserAdmin(admin.ModelAdmin):

    def SaveExecl(self, request, queryset):
        pass
    SaveExecl.short_description = "导出excel"
    actions = ["SaveExecl",]
    list_display = ('get_apply_user', 'get_event_name', 'total_price', 'checked_status', 'is_check',)
    list_editable = ('is_check',)
    list_filter = ('is_check',)
    readonly_fields = ('create_time', )

    inlines = [
        AppplyUserTypesAdmin,
    ]


admin.site.register(EventType)
admin.site.register(EventProvince)
admin.site.register(EventProject)
# admin.site.register(EventYear)

admin.site.register(HotVideo)
admin.site.site_header = '项目管理中心'
admin.site.site_title = '项目管理中心'