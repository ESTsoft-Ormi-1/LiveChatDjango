from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Post
from .forms import PostForm
from .serializers import PostSerializer, HashTagSerializer

### Post
class Index(APIView):

    def get (self, request):
        posts = Post.object.all()
        serialized_posts = PostSerializer(posts, many=True)
        return Response(serialized_posts.data)
    

class DetailView(APIView):
    
    def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)


class Write(APIView):

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            post = serializer.save(writer=request.user)
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