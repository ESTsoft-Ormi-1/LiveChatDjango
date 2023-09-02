from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.throttling import UserRateThrottle
from .models import Post, Tag, Category
from .forms import PostForm
from chat.models import Room
from chat.serializers import RoomSerializer
from .serializers import PostSerializer, TagSerializer, CategorySerializer, WriterSerializer
from user.serializers import UserSerializer
from django.db.models import Q


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
    # throttle_classes = [UserRateThrottle]

    def get(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
        
        room, created = Room.objects.get_or_create(post=post)

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
            "hit": post.hit,
            "room_data": RoomSerializer(room, context={'request': request}).data,
            "current_user": UserSerializer(request.user).data
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
            post_data = serializer.validated_data
            room_owner = request.user
            room_title = post_data.get('title')  # Use the post title as the room title
            room = Room.objects.create(owner=room_owner, name=room_title)
            # hashtags
            tags_data = serializer.validated_data.pop('tags', [])
            tags_list = []
            if tags_data:
                for tag_data in tags_data:
                    tag_name = tag_data.get('name')
                    tag, created = Tag.objects.get_or_create(name=tag_name)
                    tags_list.append(tag)

            post = Post.objects.create(writer=request.user, room=room, **post_data)
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
        serializer = PostSerializer(post, data=request.data, context={'request': request})
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
    
##카테고리
class CategoryList(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

##검색기능
class PostList(APIView):
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content', 'category__name', 'tags__name']  # 태그 이름도 검색 가능하게 추가

    def get(self, request):
        search_query = request.GET.get('search', '')
        posts = Post.objects.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query) |
            Q(category__name__icontains=search_query) | # 카테고리 이름 검색 조건 추가
            Q(tags__name__icontains=search_query)  # 태그 이름 검색 조건 추가
        )
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            category_id = request.data.get('category')  # 요청에서 카테고리 정보 가져오기
            tags = request.data.get('tags')  # 요청에서 태그 정보 가져오기
            category = Category.objects.get(id=category_id)
            post = serializer.save(category=category)
            
            if tags:
                post.tags.set(tags)  # 태그 정보 저장

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)