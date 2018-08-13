from django.db import models
from django.utils import timezone
from django.utils.html import format_html
from simditor.fields import RichTextField
from utils.models import *


# class EventProject(models.Model):
#     class Meta:
#         verbose_name = "赛事项目"
#         verbose_name_plural = "赛事项目"

#     def __str__(self):
#         return self.project

#     project = models.CharField(verbose_name="项目", max_length=50)
#     project_detail = RichTextField(verbose_name='项目介绍', null=True, blank=True)


class EventProvince(models.Model):
    class Meta:
        verbose_name = "赛事省份"
        verbose_name_plural = "赛事省份"

    def __str__(self):
        return self.province

    province = models.CharField(verbose_name="省份", max_length=50)


class EventType(models.Model):
    class Meta:
        verbose_name = "赛事类型"
        verbose_name_plural = "赛事类型"

    event_type_choices = ((0, '魔方赛事'), (1, '纸飞机'), (2, '数独'), (3, '其他'))

    def __str__(self):
        return self.type + ':' + self.event_type_choices[self.event_type][1]  # return ','.join(['类型:' + str(self.type), '资格线:' + str(self.lines), '项目价格:' + str(self.price)])

    type = models.CharField(verbose_name="类型", max_length=50)
    event_type = models.IntegerField(verbose_name='所属赛事', choices=event_type_choices, default=0)


class Events(models.Model):
    class Meta:
        verbose_name = "赛事"
        verbose_name_plural = "赛事"
        ordering = ['evnet_weight', '-event_date']

    def get_type(self):
        return self.eventtypedetail_set.all()

    evnet_weight_choices = ((0, '一级置顶'), (1, '二级置顶'), (2, '三级置顶'), (3, '四级置顶'),)
    event_type_choices = ((0, '魔方赛事'), (1, '纸飞机'), (2, '数独'), (3, '其他'))
    def __str__(self):
        return self.name

    create_date = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")
    event_date = models.DateField(verbose_name="赛事时间")
    name = models.CharField(verbose_name="赛事名称", max_length=50)
    location = models.CharField(verbose_name="位置", max_length=50)
    country = models.CharField(verbose_name='国家', max_length=100, default="中国")
    evnet_weight = models.IntegerField(verbose_name='优先级', choices=evnet_weight_choices, default=3)
    event_type = models.IntegerField(verbose_name='赛事类别', choices=event_type_choices, default=0)

    event_province = models.ForeignKey(EventProvince, on_delete=models.SET_NULL, verbose_name='赛事省份',null=True)

    def eventProvince(self):
        return self.event_province.province


class EventTypeDetail(models.Model):
    class Meta:
        verbose_name = "赛事所有类型"
        verbose_name_plural = "赛事所有类型"

    def __str__(self):
        return str(self.type)

    type = models.ForeignKey(EventType, on_delete=models.CASCADE, verbose_name='类型')
    lines = models.CharField(verbose_name='资格线', max_length=50)
    price = models.CharField(verbose_name='项目价格', max_length=50)
    event = models.ForeignKey(Events, verbose_name='赛事类型', on_delete=models.CASCADE)


class EventsDetail(models.Model):
    class Meta:
        verbose_name = "赛事详情"
        verbose_name_plural = "赛事详情"

    def __str__(self):
        return self.event.name

    event = models.OneToOneField(Events, on_delete=models.CASCADE, primary_key=True)
    evnet_org = models.CharField(verbose_name='主办方、代表', max_length=20)
    base_price = models.IntegerField(verbose_name='基础报名费', default=150)
    evnet_represent = models.CharField(verbose_name='项目及参赛资格', max_length=100)
    apply_count = models.IntegerField(verbose_name='报名人数限制', default=0)
    event_apply_begin_time = models.DateTimeField(verbose_name='报名起始时间')
    event_apply_end_time = models.DateTimeField(verbose_name='报名结束时间')
    event_about = models.TextField(verbose_name='关于比赛', null=True)


class EventRules(models.Model):
    class Meta:
        verbose_name = "赛事规则"
        verbose_name_plural = "赛事规则"

    event = models.OneToOneField(Events, on_delete=models.CASCADE, primary_key=True)
    event_rules = RichTextField(verbose_name='规则', null=True, blank=True, default='无')


class EventTraffic(models.Model):
    class Meta:
        verbose_name = "赛事交通"
        verbose_name_plural = "赛事交通"

    event = models.OneToOneField(Events, on_delete=models.CASCADE, primary_key=True)
    event_traffic = RichTextField(verbose_name='赛事交通', null=True, blank=True, default='无')
    lat = models.DecimalField(verbose_name='经纬度', max_digits=9, decimal_places=6, null=True, blank=True, default=116.404)
    lng = models.DecimalField(verbose_name='纬度', max_digits=9, decimal_places=6, null=True, blank=True, default=39.915)


class EventSc(models.Model):
    class Meta:
        verbose_name = "赛事赛程"
        verbose_name_plural = "赛事赛程"

    event = models.OneToOneField(Events, on_delete=models.CASCADE, primary_key=True)
    event_sc = RichTextField(verbose_name='赛程', null=True, blank=True, default='无')


class ApplyUser(models.Model):
    class Meta:
        verbose_name = "报名列表"
        verbose_name_plural = "报名列表"
        ordering = ['is_check', '-create_time']

    def __str__(self):
        return ""
      
    def get_apply_user_id(self):
        return self.apply_user.id

    def get_apply_user(self):
        return self.apply_user.email
    
    def get_apply_username(self):
        return self.apply_user.userprofile.username
    
    def get_apply_userphone(self):
      	return self.apply_user.userprofile.phone

    def get_event_name(self):
        verbose_name = '赛事名称'
        return self.event.name

    def get_apply_types(self):
        return ','.join([i.apply_type.type.type for i in self.applyusertypes_set.all()])
    
    def get_apply_types_list(self):
        return [i.apply_type.type.type for i in self.applyusertypes_set.all()]

    def get_apply_status(self):
        if self.is_check == 0:
            status = '未缴费'
        else:
            status = '已缴费'

        return status

    def checked_status(self):
        if self.is_check == 0:
            status = 'no'
        else:
            status = 'yes'

        return format_html('<img src="/static/admin/img/icon-{}.svg" alt="True">', status)

    checked_status.short_description = u"付费状态"
    get_apply_user.short_description = u'报名者邮箱'
    get_event_name.short_description = u'赛事名称'
    get_apply_user_id.short_description = u'报名者id'

    apply_id = models.UUIDField(primary_key=True, verbose_name='报名id')
    event = models.ForeignKey(Events, on_delete=models.SET(-1), verbose_name='报名赛事')
    apply_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='报名用户')
    create_time = models.DateField(default=timezone.now, verbose_name='报名时间')
    total_price = models.IntegerField(null=True, verbose_name='总价(自动加上赛事基础报名费)')
    remarks = models.CharField(max_length=155, null=True, blank=True, verbose_name='留言')
    is_check = models.IntegerField(default=0, choices=[[0, '未缴费'], [1, '已缴费']], verbose_name='是否缴费')

    @staticmethod
    def create(user, apply_types, **kwagrs):
        import uuid
        uuid = str(uuid.uuid1())
        try:
            event = Events.objects.get(id=kwagrs.get('event_id', 0))
        except:
            return None
        apply_user = user
        total_price = kwagrs.get('total_price', 0)
        remarks = kwagrs.get('remarks', 0)
        apply_ = ApplyUser(apply_id=uuid, event=event, apply_user=apply_user, total_price=int(total_price) + event.eventsdetail.base_price, remarks=remarks)
        

        apply_types_list = []
        
        try:
            for i in apply_types:
                apply_types_list.append(ApplyUserTypes(apply=apply_, apply_type=EventTypeDetail.objects.get(id=i)))
        except:
            return None

        apply_.save()
        ApplyUserTypes.objects.bulk_create(apply_types_list)
        return apply_


class ApplyUserTypes(models.Model):
    class Meta:
        verbose_name = "报名的类型"
        verbose_name_plural = "报名的类型"

    apply = models.ForeignKey(ApplyUser, on_delete=models.CASCADE)
    apply_type = models.ForeignKey(EventTypeDetail, on_delete=models.SET(-1))
