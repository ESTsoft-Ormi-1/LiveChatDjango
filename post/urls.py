from django.urls import path
from . import views

app_name = 'post'

urlpatterns = [
    # 글 목록
    path("", views.Index.as_view(), name='list'), #/post/
    # 글 상세 조회
    path("detail/<int:pk>/", views.DetailView.as_view(), name='list'), #/post/detail/pk/
    # 글 작성
    path("write/", views.Write.as_view(), name='write'), #/post/write/
    # 글 수정
    path("detail/<int:pk>/edit/", views.Update.as_view(), name='edit'), #/post/detail/pk/edit/
    # 글 삭제
    path("detail/<int:pk>/delete/", views.Delete.as_view(), name='delete'), #/post/detail/pk/delete/
    # 태그 작성
    # path("detail/<int:pk>/hashtag/write/", views.HashTagWrite.as_view(), name='tag-write'),
    # 태그 삭제
    # path("detail/<int:pk>/hashtag/delete/", views.HashTagDelete.as_view(), name='tag-delete'),
]