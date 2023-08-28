# user/urls.py

from django.urls import path
from .views import RegisterUserView, CustomTokenObtainPairView, LogoutUserView, FollowUserView, UnfollowUserView, UpdateProfileView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register_user'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('logout/', LogoutUserView.as_view(), name='logout_user'),
    path('follow/<int:user_id>/', FollowUserView.as_view(), name='follow_user'),
    path('unfollow/<int:user_id>/', UnfollowUserView.as_view(), name='unfollow_user'),
    path('profile/update/', UpdateProfileView.as_view(), name='update_profile'),
    # 다른 URL 매핑들도 추가 가능
]
