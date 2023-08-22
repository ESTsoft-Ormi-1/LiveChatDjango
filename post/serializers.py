from rest_framework import serializers
from .models import Post, Tag

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
        # exclude = ['writer'] # writer은 request.user로 받을 때


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'