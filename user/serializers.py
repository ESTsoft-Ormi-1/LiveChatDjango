# serializers.py

from .models import User, UserProfile
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        user = User.objects.create_user(
            email = validated_data['email'],
            password = validated_data['password']
        )
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    friends_emails = serializers.SerializerMethodField()  # 친구 id가 아닌 email을 가져오도록 직렬화합니다

    class Meta:
        model = UserProfile
        fields = ['id', 'profile_picture', 'contact_number', 'status', 'user', 'friends_emails']

    def get_friends_emails(self, obj):
        # friends 필드에 대해 email을 가져오는 로직을 작성합니다.
        return [friend.email for friend in obj.friends.all()]


class UserFriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']