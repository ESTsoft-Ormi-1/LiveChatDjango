from rest_framework import serializers
from .models import Post, HashTag

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        # fields = '__all__'
        exclude = ['writer'] # writer은 request.user로 받을 때


class HashTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = HashTag
        fields = '__all__'