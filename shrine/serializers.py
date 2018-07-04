from rest_framework import serializers
from .models import *
from cms.models import *


class UserProfileRecodeX(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username', 'sex', 'country']


class UserRecodeX(serializers.ModelSerializer):
    userprofile = UserProfileRecodeX(read_only=True)  # many=True 是一对多 而这个是一对一关系 哎呀

    # users = serializers.StringRelatedField(read_only=True) #跟着model_str_走?

    class Meta:
        model = User
        fields = ['id', 'userprofile']


class ContestRecodeX(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = ['event_date', 'name', 'location', 'country', 'eventProvince', 'evnet_weight']


class RankRecodeX(serializers.ModelSerializer):
    class Meta:
        model = Authority
        fields = ['username_str', 'events_str', 'eventType_str', 'single', 'turn', 'recent', 'award']
