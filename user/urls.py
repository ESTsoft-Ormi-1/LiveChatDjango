from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import TestJWTAuth
from .views import UserProfileView, CustomRegisterView, CustomLoginView, CustomLogoutView, AddFriendView, FriendProfileView, DeleteFriendView, SearchFriendsView,  UserFriendView

urlpatterns = [
    #path('', include('dj_rest_auth.urls')),
    path('registration/', CustomRegisterView.as_view(), name='custom_register'),  # 커스텀 회원가입 뷰
    path('login/', CustomLoginView.as_view(), name='custom_login'),  # 커스텀 로그인 뷰
    path('logout/', CustomLogoutView.as_view(), name='custom_logout'),  # 커스텀 로그아웃 뷰
    #path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # JWT 토큰 생성 URL 추가
    path('test-jwt-auth/', TestJWTAuth.as_view(), name='test_jwt_auth'), #JWT 토큰 인증 URL
    path('profile/', UserProfileView.as_view(), name='user-profile'), #프로필 조회
    path('add-friend/', AddFriendView.as_view(), name='add_friend'),  # 친구 추가 뷰
    path('friends/', UserFriendView.as_view(), name='friends-list'), #친구 목록 조회
    path('friend-profile/<int:friend_id>/', FriendProfileView.as_view(), name='friend_profile'),  # 친구 프로필 조회 뷰
    path('delete-friend/', DeleteFriendView.as_view(), name='delete_friend'), # 친구 삭제
    path('search-friends/', SearchFriendsView.as_view(), name='search_friends'), #친구 검색
    #path('delete-account/', DeleteAccountView.as_view(), name='delete_account'), 
]
