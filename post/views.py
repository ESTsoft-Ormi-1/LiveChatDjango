from rest_framework import viewsets
from .serializers import PostSerializer
from django.shortcuts import render
from django.views import View
from .models import Post
from django.db.models import Q
# Create your views here.


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


# 게시물 검색
class Post_search(View):
    def get(self,request):
        if 'kw' in request.GET:
            query = request.GET.get('kw')
            posts = Post.objects.all().filter(
                Q(title__icontains=query) |
                Q(content__icontains=query)
            )

        return render(request, 'post/post_search.html', {'query':query, 'posts':posts})

