from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.throttling import UserRateThrottle
from .models import Post, Tag
from .forms import PostForm
from .serializers import PostSerializer, TagSerializer, WriterSerializer

### Post
class Index(APIView):
    permission_classes = [AllowAny] 

    def get (self, request):
        posts = Post.objects.all()
        serialized_posts = PostSerializer(posts, many=True)
        return Response(serialized_posts.data)
    

class DetailView(APIView):
    # 인증된 사용자만 접근 가능
    permission_classes = [IsAuthenticated] 
    # 사용자 요청 속도 제한 설정
    throttle_classes = [UserRateThrottle]

    def get(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

        # 조회수 증가
        post.hit += 1
        post.save()

        serialized_post = PostSerializer(post).data
        serialized_writer = WriterSerializer(request.user).data
        
        tags = post.tags.all()
        serialized_tags = TagSerializer(tags, many=True).data

        data = {
            "post_id": pk,
            "title": serialized_post['title'],
            "content": serialized_post['content'], 
            "writer": serialized_writer,
            "tags": serialized_tags,
            "hit": post.hit
        }
        
        return Response(data)


class Write(APIView):
    # 인증된 사용자만 접근 가능
    permission_classes = [IsAuthenticated] 
    # 사용자 요청 속도 제한 설정
    throttle_classes = [UserRateThrottle]

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

            post = serializer.save(writer=request.user) # writer=request.user
            post.tags.set(tags_list)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class Update(APIView):
    # 인증된 사용자만 접근 가능
    permission_classes = [IsAuthenticated] 
    # 사용자 요청 속도 제한 설정
    throttle_classes = [UserRateThrottle]
    
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
    