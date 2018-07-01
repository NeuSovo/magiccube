from rest_framework import serializers
from .models import *
from cms.models import *



class UserProfileRecodeX(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username', 'sex', 'country']


class UserRecodeX(serializers.ModelSerializer):
    users = UserProfileRecodeX(read_only=True)  # many=True 是一对多 而这个是一对一关系 哎呀

    # user = serializers.StringRelatedField(many=True) #跟着model_str_走?

    class Meta:
        model = User
        fields = ['id', 'users']


class ContestRecodeX(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = ['event_date', 'name', 'location', 'country', 'event_province', 'evnet_weight']
