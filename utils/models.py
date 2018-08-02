import requests
from django.db import models
from django.contrib.auth.hashers import make_password, check_password
# Create your models here.

class User(models.Model):

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = "用户信息"

    def __str__(self):
        return self.email

    def username(self):
        return self.userprofile.username

    # 为了WeChat User 改为null
    email = models.EmailField(verbose_name='邮箱', max_length=100, null=True)
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

    @staticmethod
    def change_user_password(old_password=None, password=None, user=None):
        if check_password(old_password, user.password):
            user.password = make_password(password)
            user.save()
            return True
        return False


class UserProfile(models.Model):

    class Meta:
        verbose_name = "用户详情"
        verbose_name_plural = "用户详情"
        ordering = ['username']


    def __str__(self):
        return self.user.email

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    username = models.CharField(verbose_name='姓名', max_length=100)
    nick_name = models.CharField(verbose_name='微信昵称', null=True, blank=True, max_length=120)
    avatar = models.ImageField(verbose_name='头像', default='none', upload_to="avatar")
    sex = models.CharField(max_length=20, null=True,
                           blank=True, verbose_name='性别')
    birthday = models.CharField(
        max_length=20, null=True, blank=True, verbose_name='生日')
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
        self.username = kwagrs.get('username') or ''
        self.sex = kwagrs.get('sex') or ''
        self.birthday = kwagrs.get('birthday') or ''
        self.phone = kwagrs.get('phone') or 0
        self.country = kwagrs.get('country') or ''
        self.province = kwagrs.get('province') or ''
        self.city = kwagrs.get('city') or ''
        self.paperwork_type = kwagrs.get('paperwork_type') or ''
        self.paperwork_id = kwagrs.get('paperwork_id') or 0
        self.save()


class UserPicture(models.Model):

    class Meta:
        verbose_name = "用户相册"
        verbose_name_plural = "用户相册"

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    picture = models.ImageField(verbose_name='相册', null=True, blank=True, upload_to="picture")


class UserFirst(models.Model):

    class Meta:
        verbose_name = "用户首选项目"
        verbose_name_plural = "用户首选项目s"


    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    project = models.CharField(verbose_name='首选项目', null=True, blank=True, max_length=30)
    

class WeChatUser(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='用户')
    openid = models.CharField(verbose_name='微信id', max_length=50, null=True, blank=True)
    refresh_token = models.CharField(verbose_name='微信验证token', max_length=120, null=True, blank=True)
    access_token = models.CharField(verbose_name='token', max_length=120)
    unionid = models.CharField(verbose_name='单应用唯一id',null=True, max_length=120)


    def update_profile(self, *args, **kwagrs):
        self.user.useprofile.nick_name = kwagrs.get['nick_name']
        self.user.useprofile.sex = '男' if kwagrs.get['sex'] == 1 else '女'
        self.user.useprofile.country = kwagrs.get('country')
        self.user.useprofile.province = kwagrs.get('province')
        self.user.useprofile.city = kwagrs.get('city')
        # self.user.userprofile.avatar = requests.get(kwagrs.get('headimgurl')) # pass
        self.user.useprofile.save()
        self.refresh_token = kwagrs.get('update_profile')
        self.access_token = kwagrs.get('update_profile')
        self.unionid = kwagrs.get('update_profile')
        self.save()

