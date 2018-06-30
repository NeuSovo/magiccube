from django.contrib import admin
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
from .models import *
import csv
import codecs


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
        password = request.POST['password'][0]
        password = make_password(password)
        obj.password = password
        obj.save()


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    '''
        Admin View for News
    '''
    list_display = ('title', 'create_user', 'create_time', 'is_top')
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
    list_display = ('event_date', 'name', 'location',
                    'evnet_weight', 'event_province', 'event_project')
    list_filter = ('evnet_weight', 'event_date')
    inlines = [
        EventsDetailAdmin,
        EventsTypeAdmin,
        EventsRulesAdmin,
        EventsTrafficAdmin,
        EventsScAdmin,
    ]
    # raw_id_fields = ('',)
    # readonly_fields = ('',)
    # search_fields = ('',)


class ApplyEventsFilter(admin.SimpleListFilter):
    title = (u'报名赛事')
    parameter_name = 'event'

    def lookups(self, request, model_admin):
        return [[i.id, i.name] for i in Events.objects.all()]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(event__id=self.value())


class AppplyUserTypesAdmin(admin.TabularInline):
    model = ApplyUserTypes


@admin.register(ApplyUser)
class ApplyUserAdmin(admin.ModelAdmin):

    def export_as_csv_action(description="1", fields=None, exclude=None, header=True):
        def export_as_csv(modeladmin, request, queryset):
            opts = modeladmin.model._meta
            if not fields:
                field_names = [filed for filed in opts]
            else:
                field_names = fields

            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment;filename=result.csv'
            response.write(codecs.BOM_UTF8)
            writer = csv.writer(response)
            if header:
                writer.writerow(header)

            for obj in queryset:
                row = [getattr(obj, field)() if callable(
                    getattr(obj, field)) else getattr(obj, field) for field in field_names]
                writer.writerow(row)

            return response
        export_as_csv.short_description = description
        return export_as_csv

    # SaveExecl.short_description = "导出excel"
    actions = [export_as_csv_action("导出excel", fields=[ 'create_time', 'apply_user', 'get_event_name', 'total_price', 'remarks', 'get_apply_types', 'get_apply_status'], 
                                    header=['报名时间', '报名者邮箱', '报名赛事', '总价', '留言', '报名赛事' '是否缴费'])]

    list_display = ('create_time', 'get_apply_user', 'get_event_name',
                    'total_price', 'checked_status', 'is_check',)
    list_editable = ('is_check',)
    list_filter = ('is_check', ApplyEventsFilter)
    readonly_fields = ('create_time', 'apply_id')

    search_fields = ('apply_user__email',)

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
