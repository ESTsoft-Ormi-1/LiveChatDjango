from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        post = Post # 모델 설정
        fields = ('id','title','content','writer','created_at','updated_at','hit') # 필드 설정