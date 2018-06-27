from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.utils.html import format_html


class News(models.Model):

    is_top_choices =(
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
    is_top = models.IntegerField(verbose_name='是否置顶', default=0, choices=is_top_choices)


class EventYear(models.Model):

    class Meta:
        verbose_name = "赛事年份"
        verbose_name_plural = "赛事年份"

    year = models.CharField(verbose_name="年份", max_length=10)

    def __str__(self):
        return self.year


class EventProject(models.Model):

    class Meta:
        verbose_name = "赛事项目"
        verbose_name_plural = "赛事项目"

    def __str__(self):
        return self.project

    project = models.CharField(verbose_name="项目", max_length=50)



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

    type = models.CharField(verbose_name="类型", max_length=50)
    

class Events(models.Model):

    class Meta:
        verbose_name = "赛事"
        verbose_name_plural = "赛事"
        ordering = ['evnet_weight','-event_date']

    evnet_weight_choices = (
        (0, '一级置顶'),
        (1, '二级置顶'),
        (2, '三级置顶'),
        (3, '四级置顶'),
        )

    def __str__(self):
        return self.name

    event_date = models.DateTimeField(auto_now_add=False, verbose_name="日期")
    name =  models.CharField(verbose_name="名称", max_length=50)
    location = models.CharField(verbose_name="位置", max_length=50)
    country = models.CharField(verbose_name='国家', max_length=100, default="中国")
    evnet_weight = models.IntegerField(verbose_name='优先级', choices=evnet_weight_choices, default=3)
    can_apply_count = models.IntegerField(verbose_name='可报名人数', default=0)

    event_year = models.ForeignKey(EventYear, on_delete=models.SET(-1), verbose_name='赛事年份', default=-1)
    event_type = models.ManyToManyField(EventType, verbose_name='赛事类型', default=-1)
    event_province = models.ForeignKey(EventProvince, on_delete=models.SET(-1), verbose_name='赛事省份', default=-1)
    event_project = models.ForeignKey(EventProject, on_delete=models.SET(-1), verbose_name='赛事项目', default=-1)


class EventsDetail(models.Model):

    class Meta:
        verbose_name = "赛事详情"
        verbose_name_plural = "赛事详情"

    def __str__(self):
        return ''

    id = models.OneToOneField(Events, on_delete=models.CASCADE, primary_key=True)
    event_detail = models.TextField(verbose_name='赛事详情', null=True)
    event_rules = models.TextField(verbose_name='赛事规则', null=True)
    event_traffic = models.ImageField(upload_to='img', verbose_name='赛事交通', null=True)


class HotVideo(models.Model):

    class Meta:
        verbose_name = "精彩视频"
        verbose_name_plural = "精彩视频"

    title = models.CharField(verbose_name="标题", max_length=50)
    video_url = models.URLField(verbose_name="链接")


class User(models.Model):

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = "用户信息"

    def __str__(self):
        return self.email

    def username(self):
        return self.userprofile.username

    email = models.CharField(verbose_name='邮箱', max_length=100)
    password = models.CharField(verbose_name='密码', max_length=50)
    is_email_check = models.IntegerField(verbose_name='邮箱是否验证', choices=[[0, '未验证'], [1, '已发送邮件'], [2, '已验证']])
    reg_date = models.DateTimeField(auto_now_add=True, verbose_name="注册时间")


    @staticmethod
    def is_exist_user(email):
        user = User.get_user_by_email(email)
        return user is not None


    @staticmethod
    def reg_user(body):
        try:
            email = body.get('email')
            username = body.get('username')
            password = make_password(body.get('password'))
        except Exception as e:
            return None

        user = User(email=email, password=password, is_email_check=0)
        user.save()
        UserProfile(user=user, username=username).save()

        return user

    @staticmethod
    def login_user(body):
        email = body.get('email')
        password = body.get('password')
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

    user = models.OneToOneField(User,on_delete=models.CASCADE, primary_key=True)
    username = models.CharField(verbose_name='姓名', max_length=100)
    sex = models.CharField(max_length=20, null=True, blank=True)
    # 待定


class ApplyUser(models.Model):

    class Meta:
        verbose_name = "报名列表"
        verbose_name_plural = "报名列表"

    def __str__(self):
        return ""

    def get_apply_user(self):
        return self.apply_user.email

    def get_event_name(self):
        verbose_name = '赛事名称'
        return self.event.name

    def checked_status(self):
        if self.is_check == 0:
            color_code ='red'
            text = u'未缴费'
        else:
            color_code = 'green'
            text = u'已缴费'

        return format_html(
            '<span style="color: {};">{}</span>',
            color_code,
            text,
        )
    checked_status.short_description = u"状态"
    get_apply_user.short_description = u'报名者邮箱'
    get_event_name.short_description = u'赛事名称'

    apply_id  = models.UUIDField(primary_key=True)
    event = models.ForeignKey(Events, on_delete=models.SET(-1), verbose_name='报名赛事')
    apply_user = models.ForeignKey(User, on_delete=models.SET(-1), verbose_name='报名用户')
    create_time = models.DateTimeField(auto_now_add=True)
    total_price = models.IntegerField(null=True, verbose_name='总价')
    remarks = models.CharField(max_length=155, null=True, blank=True, verbose_name='留言')
    is_check = models.IntegerField(default=0, choices=[[0, '未缴费'], [1, '已缴费']], verbose_name='是否缴费')

