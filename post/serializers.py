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
    
    def create(self, validated_data):
        # 현재 로그인한 사용자를 작성자로 설정
        validated_data['writer'] = self.context['request'].user
        return super().create(validated_data)

class WriterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email',)

