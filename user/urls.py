from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import TestJWTAuth
urlpatterns = [
    path('', include('dj_rest_auth.urls')),
    path('registration/', include('dj_rest_auth.registration.urls')),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # JWT 토큰 생성 URL 추가
    path('test-jwt-auth/', TestJWTAuth.as_view(), name='test_jwt_auth'),
]
