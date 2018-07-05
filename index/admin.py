from django.contrib import admin
from .models import *
# Register your models here.

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

admin.site.register(JoinOur)
admin.site.register(HotVideo)
admin.site.register(LunBo)