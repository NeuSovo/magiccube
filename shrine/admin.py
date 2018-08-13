from django.contrib import admin
from .models import Authority
@admin.register(Authority)
class AuthorityAdmin(admin.ModelAdmin):
    list_display = ['username', 'events_', 'event_type', 'turn', 'single', 'recent']
    raw_id_fields = ('username',)

    def user_(self, obj):
        return obj.username.username

    def events_(self, obj):
        return obj.events.name

    def event_type(self, obj):
        return obj.eventType.type

    user_.short_description = '用户'
    events_.short_description = '赛事'
    event_type.short_description = '类型'

    # def save_model(self, request, obj, form, change):
    #     userID = request.POST['username']
    #     try:
    #         history = UserHistory.objects.get(name=userID)
    #         history.detail = history.detail + obj.single + ' '
    #         history.count = history.count + obj.single
    #         history.join = history.join + 1
    #         history.average = history.count / history.join
    #     except:
    #         history = UserHistory(name_id=int(userID), count=obj.single, detail='{}'.format(obj.single), join=1,
    #                               average=obj.single)
    #     history.save()
    #     obj.save()
