from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import TestJWTAuth
from .views import UserProfileView, CustomRegisterView, CustomLoginView, CustomLogoutView

urlpatterns = [
    #path('', include('dj_rest_auth.urls')),
    path('registration/', CustomRegisterView.as_view(), name='custom_register'),  # 커스텀 회원가입 뷰
    path('login/', CustomLoginView.as_view(), name='custom_login'),  # 커스텀 로그인 뷰
    path('logout/', CustomLogoutView.as_view(), name='custom_logout'),  # 커스텀 로그아웃 뷰
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # JWT 토큰 생성 URL 추가
    path('test-jwt-auth/', TestJWTAuth.as_view(), name='test_jwt_auth'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
]
