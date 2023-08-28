from django.contrib import admin
from django.urls import path, include  # include 추가

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('user.urls')),  # 앱의 URL 패턴을 등록
]