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
        post = Post.objects.prefetch_related('hashtag_set').get(pk=pk)
        
        tags = post.tag_set.all()
        serialized_tags = TagSerializer(tags, many=True).data

        data = {
            "post_id": pk,
            "tags": serialized_tags
        }
        
        return Response(data)


class Write(APIView):

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            # hashtag
            tags_data = request.data.get('tags', [])
            tags_list = []
            if tags_data:
                if isinstance(tags_data, str):
                    tags_data = [tags_data]
                for tag_name in tags_data:
                    tag, created = Tag.objects.get_or_create(name=tag_name)
                    tags_list.append(tag)

            post = serializer.save(writer=request.user)
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
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Delete(APIView):
    
    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        post.delete()
        return Response({ 'msg': 'Post deleted' }, status=status.HTTP_204_NO_CONTENT)
    