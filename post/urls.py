from django.urls import path
from . import views

app_name = 'post'

urlpatterns = [

    # 검색
    path('post_search/', views.Post_search.as_view(), name='post_search'),


]