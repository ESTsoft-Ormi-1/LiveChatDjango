from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Post, Tag
from .forms import PostForm
from .serializers import PostSerializer, TagSerializer

### Post
class Index(APIView):

    def get (self, request):
        posts = Post.objects.all()
        serialized_posts = PostSerializer(posts, many=True)
        return Response(serialized_posts.data)
    

class DetailView(APIView):
    
    def get(self, request, pk):
        post = Post.objects.prefetch_related('tags').get(pk=pk)
        serialized_post = PostSerializer(post).data
        
        tags = post.tags.all()
        serialized_tags = TagSerializer(tags, many=True).data

        data = {
            "post_id": pk,
            "title": serialized_post['title'],
            "content": serialized_post['content'], 
            "tags": serialized_tags
        }
        
        return Response(data)


class Write(APIView):

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            # hashtags
            tags_data = serializer.validated_data.pop('tags', [])
            tags_list = []
            if tags_data:
                for tag_data in tags_data:
                    tag_name = tag_data.get('name')
                    tag, created = Tag.objects.get_or_create(name=tag_name)
                    tags_list.append(tag)

            post = serializer.save()  # writer=request.user
            post.tags.set(tags_list)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class Update(APIView):
    
    def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            # 태그를 수정을 위해 기존 태그 제거
            post.tags.clear()
            # 기존 태그 불러오기
            tag_names = request.data.get('tags', [])
            # 새로운 태그 추가
            for tag_name in tag_names:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                post.tags.add(tag)

            # 태그 삭제
            tags_to_delete = request.data.get('tags_to_delete', [])
            # 선택적으로 삭제할 태그를 제거
            if tags_to_delete:
                post.tags.remove(*tags_to_delete)

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Delete(APIView):
    
    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        post.delete()
        return Response({ 'msg': 'Post deleted' }, status=status.HTTP_204_NO_CONTENT)
    