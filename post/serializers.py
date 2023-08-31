from rest_framework import serializers
from .models import Post, Tag
from user.models import User

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name',)


class PostSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    class Meta:
        model = Post
        fields = '__all__'
        # exclude = ['writer']

class WriterSerializer(serializers.ModelSerializer):
    email = None

    class Meta:
        model = User
        exclude = ('email',)

