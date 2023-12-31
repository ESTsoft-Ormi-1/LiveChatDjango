from rest_framework import serializers
from .models import Post, Tag, Category, User

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name',)


class PostSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    writer_nickname = serializers.CharField(source='writer.userprofile.nickname', read_only=True)
    writer_profile_picture = serializers.ImageField(source='writer.userprofile.profile_picture', read_only=True)
    class Meta:
        model = Post
        fields = '__all__'
        # exclude = ['writer']
    
    # def create(self, validated_data):
    #     # 현재 로그인한 사용자를 작성자로 설정
    #     validated_data['writer'] = self.context['request'].user
    #     return super().create(validated_data)
    
    def update(self, instance, validated_data):
        validated_data['writer'] = self.context['request'].user
        return super().update(instance, validated_data)

class WriterSerializer(serializers.ModelSerializer):
    nickname = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'nickname')

    def get_nickname(self, obj):
        try:
            return obj.userprofile.nickname
        except User.UserProfile.DoesNotExist:
            return None


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'