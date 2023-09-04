# serializers.py

from .models import User, UserProfile
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework import serializers
from allauth.account import app_settings as allauth_settings
from allauth.utils import email_address_exists
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from allauth.socialaccount import providers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        user = User.objects.create_user(
            nickname = validated_data['nickname'],
            email = validated_data['email'],
            password = validated_data['password']
        )
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    friends_emails = serializers.SerializerMethodField()  # 친구 id가 아닌 

    class Meta:
        model = UserProfile
        fields = ['id', 'profile_picture', 'contact_number', 'status', 'user', 'friends_emails', 'is_private', 'nickname',]

    def get_friends_emails(self, obj):
        # friends 필드에 대해 email을 가져오는 로직을 작성합니다.
        return [friend.email for friend in obj.friends.all()]


class UserFriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']