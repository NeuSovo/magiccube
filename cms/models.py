from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.utils.html import format_html
from simditor.fields import RichTextField


class News(models.Model):

    is_top_choices = (
        (0, '不置顶'),
        (1, '置顶')
    )

    class Meta:
        verbose_name = "新闻"
        verbose_name_plural = "新闻"
        ordering = ['-is_top', '-create_time']

    def __str__(self):
        return self.title

    title = models.CharField(verbose_name="标题", max_length=50)
    img = models.ImageField(verbose_name='图片', default='none', upload_to="img")
    content = models.TextField(verbose_name="内容")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    create_user = models.CharField(verbose_name="播报员", max_length=30)
    is_top = models.IntegerField(
        verbose_name='是否置顶', default=0, choices=is_top_choices)
    news_url = models.URLField(verbose_name="链接")


class HotVideo(models.Model):

    class Meta:
        verbose_name = "精彩视频"
        verbose_name_plural = "精彩视频"
        ordering = ['-add_time']

    title = models.CharField(verbose_name="标题", max_length=50)
    video_url = models.URLField(verbose_name="链接")
    add_time = models.DateTimeField(auto_now_add=True)

class EventProject(models.Model):

    class Meta:
        verbose_name = "赛事项目"
        verbose_name_plural = "赛事项目"

    def __str__(self):
        return self.project

    project = models.CharField(verbose_name="项目", max_length=50)
    project_detail = RichTextField(verbose_name='项目介绍', null=True, blank=True)


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

    def __str__(self):
        return self.type
        # return ','.join(['类型:' + str(self.type), '资格线:' + str(self.lines), '项目价格:' + str(self.price)])

    type = models.CharField(verbose_name="类型", max_length=50)


class Events(models.Model):

    class Meta:
        verbose_name = "赛事"
        verbose_name_plural = "赛事"
        ordering = ['evnet_weight', '-event_date']

    def get_type(self):
        return self.eventtypedetail_set.all()

    evnet_weight_choices = (
        (0, '一级置顶'),
        (1, '二级置顶'),
        (2, '三级置顶'),
        (3, '四级置顶'),
    )

    def __str__(self):
        return self.name

    event_date = models.DateTimeField(auto_now_add=True, verbose_name="日期")
    name = models.CharField(verbose_name="赛事名称", max_length=50)
    location = models.CharField(verbose_name="位置", max_length=50)
    country = models.CharField(verbose_name='国家', max_length=100, default="中国")
    evnet_weight = models.IntegerField(
        verbose_name='优先级', choices=evnet_weight_choices, default=3)

    event_province = models.ForeignKey(
        EventProvince, on_delete=models.SET(-1), verbose_name='赛事省份')
    event_project = models.ForeignKey(
        EventProject, on_delete=models.SET(-1), verbose_name='赛事项目')


class EventTypeDetail(models.Model):
    class Meta:
        verbose_name = "赛事所有类型"
        verbose_name_plural = "赛事所有类型"

    def __str__(self):
        return self.type.type

    type = models.ForeignKey(
        EventType, on_delete=models.CASCADE, verbose_name='类型')
    lines = models.CharField(verbose_name='资格线', max_length=50)
    price = models.CharField(verbose_name='项目价格', max_length=50)
    event = models.ForeignKey(
        Events, verbose_name='赛事类型', on_delete=models.CASCADE)


class EventsDetail(models.Model):

    class Meta:
        verbose_name = "赛事详情"
        verbose_name_plural = "赛事详情"

    def __str__(self):
        return ''

    event = models.OneToOneField(
        Events, on_delete=models.CASCADE, primary_key=True)
    evnet_org = models.CharField(verbose_name='主办方、代表', max_length=20)
    evnet_represent = models.CharField(verbose_name='项目及参赛资格', max_length=100)
    apply_count = models.IntegerField(verbose_name='报名人数限制', default=0)
    event_apply_begin_time = models.DateTimeField(verbose_name='报名起始时间')
    event_apply_end_time = models.DateTimeField(verbose_name='报名结束时间')
    event_about = models.TextField(verbose_name='关于比赛', null=True)


class EventRules(models.Model):
    class Meta:
        verbose_name = "赛事规则"
        verbose_name_plural = "赛事规则"
    event = models.OneToOneField(
        Events, on_delete=models.CASCADE, primary_key=True)
    event_rules = RichTextField(verbose_name='规则', null=True, blank=True)


class EventTraffic(models.Model):
    class Meta:
        verbose_name = "赛事交通"
        verbose_name_plural = "赛事交通"
    event = models.OneToOneField(
        Events, on_delete=models.CASCADE, primary_key=True)
    event_traffic = RichTextField(verbose_name='赛事交通', null=True, blank=True)


class EventSc(models.Model):
    class Meta:
        verbose_name = "赛事赛程"
        verbose_name_plural = "赛事赛程"

    event = models.OneToOneField(
        Events, on_delete=models.CASCADE, primary_key=True)
    event_sc = RichTextField(verbose_name='赛程', null=True, blank=True)


class User(models.Model):

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = "用户信息"

    def __str__(self):
        return self.email

    def username(self):
        return self.userprofile.username

    email = models.CharField(verbose_name='邮箱', max_length=100, unique=True)
    password = models.TextField(verbose_name='密码')
    is_email_check = models.IntegerField(verbose_name='邮箱是否验证', choices=[
                                         [0, '未验证'], [1, '已发送邮件'], [2, '已验证']])
    reg_date = models.DateTimeField(auto_now_add=True, verbose_name="注册时间")

    @staticmethod
    def is_exist_user(email):
        user = User.get_user_by_email(email)
        return user is not None

    @staticmethod
    def reg_user(email, username, password):
        password = make_password(password)
        user = User(email=email, password=password, is_email_check=0)
        user.save()
        UserProfile(user=user, username=username).save()

        return user

    @staticmethod
    def login_user(email, password):
        # email = body.get('email')
        # password = body.get('password')
        tmp_user = User.get_user_by_email(email)

        if tmp_user:
            if check_password(password, tmp_user.password):
                return tmp_user

        return None

    @staticmethod
    def get_user_by_id(id):
        try:
            user = User.objects.get(id=id)
        except Exception as e:
            raise e
            return None

        return user

    @staticmethod
    def get_user_by_email(email):
        try:
            user = User.objects.get(email=email)
        except Exception as e:
            return None

        return user


class UserProfile(models.Model):

    class Meta:
        verbose_name = "用户详情"
        verbose_name_plural = "用户详情"

    def __str__(self):
        return self.user.email

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    username = models.CharField(verbose_name='姓名', max_length=100)
    sex = models.CharField(max_length=20, null=True,
                           blank=True, verbose_name='性别')
    birthday = models.CharField(
        max_length=20, null=True, blank=True, verbose_name='国家')
    phone = models.BigIntegerField(null=True, blank=True, verbose_name='电话')
    country = models.CharField(
        max_length=20, null=True, blank=True, verbose_name='地区')
    province = models.CharField(
        max_length=20, null=True, blank=True, verbose_name='省份')
    city = models.CharField(max_length=20, null=True,
                            blank=True, verbose_name='城市')

    paperwork_type = models.CharField(
        max_length=20, default="身份证", verbose_name='证件类型')

    paperwork_id = models.BigIntegerField(
        verbose_name='证件号', null=True, blank=True)
    # 待定

    def update(self, **kwagrs):
        self.username = kwagrs.get('username', '')
        self.sex = kwagrs.get('sex', '')
        self.birthday = kwagrs.get('birthday', '')
        self.phone = kwagrs.get('phone', 0)
        self.country = kwagrs.get('country', '')
        self.province = kwagrs.get('province', '')
        self.city = kwagrs.get('city', '')
        self.paperwork_type = kwagrs.get('paperwork_type', '')
        self.paperwork_id = kwagrs.get('paperwork_id', 0)
        self.save()


class ApplyUser(models.Model):

    class Meta:
        verbose_name = "报名列表"
        verbose_name_plural = "报名列表"
        ordering = ['is_check', '-create_time']

    def __str__(self):
        return ""

    def get_apply_user(self):
        return self.apply_user.email

    def get_event_name(self):
        verbose_name = '赛事名称'
        return self.event.name

    def get_apply_types(self):
        return ','.join([i.apply_type.type.type for i in self.applyusertypes_set.all()])

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

        return format_html(
            '<img src="/static/admin/img/icon-{}.svg" alt="True">',
            status
        )
    checked_status.short_description = u"付费状态"
    get_apply_user.short_description = u'报名者邮箱'
    get_event_name.short_description = u'赛事名称'

    apply_id = models.UUIDField(primary_key=True, verbose_name='报名id')
    event = models.ForeignKey(
        Events, on_delete=models.SET(-1), verbose_name='报名赛事')
    apply_user = models.ForeignKey(
        User, on_delete=models.SET(-1), verbose_name='报名用户')
    create_time = models.DateTimeField(auto_now_add=True)
    total_price = models.IntegerField(null=True, verbose_name='总价')
    remarks = models.CharField(
        max_length=155, null=True, blank=True, verbose_name='留言')
    is_check = models.IntegerField(
        default=0, choices=[[0, '未缴费'], [1, '已缴费']], verbose_name='是否缴费')

    @staticmethod
    def create(user, apply_types, **kwagrs):
        import uuid
        uuid = str(uuid.uuid1())
        event = Events.objects.get(id=kwagrs.get('event_id', 0))
        apply_user = user
        total_price = kwagrs.get('total_price', 0)
        remarks = kwagrs.get('remarks', 0)
        apply_ = ApplyUser(apply_id=uuid, event=event, apply_user=apply_user,
                           total_price=total_price, remarks=remarks)
        apply_.save()

        apply_types_list = []
        for i in apply_types:
            apply_types_list.append(ApplyUserTypes(
                apply=apply_, apply_type=EventTypeDetail.objects.get(id=i)))

        ApplyUserTypes.objects.bulk_create(apply_types_list)
        return apply_


class ApplyUserTypes(models.Model):
    class Meta:
        verbose_name = "报名的类型"
        verbose_name_plural = "报名的类型"

    apply = models.ForeignKey(ApplyUser, on_delete=models.CASCADE)
    apply_type = models.ForeignKey(EventTypeDetail, on_delete=models.SET(-1))


class UserParagraph(models.Model):
    class Meta:
        verbose_name = "用户段位认证"
        verbose_name_plural = "用户段位认证"
        ordering = ['user']

    def __str__(self):
        return self.user.username

    @property
    def username(self):
        return self.user.username
    
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="用户")
    rz_date = models.DateTimeField(auto_now_add=True, verbose_name="认证时间")
    paragraph = models.CharField(max_length=100, verbose_name="段位")


class RzgParagraph(models.Model):
    class Meta:
        verbose_name = "认证官"
        verbose_name_plural = "认证官"
        ordering = ['name']

    country = models.CharField(max_length=50, verbose_name="地区")
    name = models.CharField(max_length=50, verbose_name="姓名")
    sex = models.CharField(max_length=50, verbose_name="性别")
    phone = models.BigIntegerField(verbose_name="电话")
    wechat = models.CharField(max_length=100, verbose_name='微信')


class JlParagraph(models.Model):
    class Meta:
        verbose_name = "教练证书"
        verbose_name_plural = "教练证书"
        ordering = ['name']

    country = models.CharField(max_length=50, verbose_name="地区")
    name = models.CharField(max_length=50, verbose_name="姓名")
    paragraph = models.CharField(max_length=100, verbose_name="级别")


class UserScore(models.Model):
    class Meta:
        verbose_name='成绩详情'
        verbose_name='成绩详情'

    user = models.ForeignKey(UserProfile, on_delete=models.SET(-1) )
    event = models.ForeignKey(Events, on_delete=models.SET(-1))
    score_type = models.ForeignKey(EventType, on_delete=models.SET(-1), verbose_name='成绩类型')
    score = models.DecimalField(max_digits=10,decimal_places=3, verbose_name='成绩')
