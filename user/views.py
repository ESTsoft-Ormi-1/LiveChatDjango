from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView 
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import UserProfileSerializer, UserSerializer, UserFriendSerializer
from .models import UserProfile, User
from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView, LogoutView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import Q
from django.contrib.auth import authenticate


##회원가입
class CustomRegisterView(RegisterView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == status.HTTP_201_CREATED:
            user_email = response.data['email']
            response.data['message'] = f"{user_email}님 회원가입이 완료되었습니다."

            # 회원가입 후 프로필 생성
            user = User.objects.get(email=user_email)  # 이 부분을 추가해 user 객체를 가져옴
            UserProfile.objects.create(user=user)
            user_profile = UserProfile.objects.get(user=user)
            serializer = UserProfileSerializer(user_profile)
            response.data['profile'] = serializer.data

        return response


##로그인
class CustomLoginView(LoginView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == status.HTTP_200_OK:
            user_email = self.user.email
            response.data['message'] = f"{user_email}님 환영합니다."

            user_profile = UserProfile.objects.get(user=self.user)
            serializer = UserProfileSerializer(user_profile)
            response.data['profile'] = serializer.data
            
            # JWT 토큰 생성 및 응답에 추가
            refresh = RefreshToken.for_user(self.user)
            response.data['refresh'] = str(refresh)
            response.data['access'] = str(refresh.access_token)
        
        return response


##로그아웃
class CustomLogoutView(LogoutView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        response.data = {
            "message": "로그아웃이 완료되었습니다."
        }
        return response


#Test Code
class TestJWTAuth(APIView):
    permission_classes = [IsAuthenticated]  # 이 view를 호출하기 위해서는 인증이 필요하다는 뜻 입니다(DRF 자체에서 아무나 들어올 수 없도록 막아주는 기본 기능입니다.)

    def get(self, request):
        user = request.user  # 현재 인증된 사용자 정보 가져오기
        return Response({"message": f"안녕하세요, {user}님! JWT인증이 완료되었습니다!."})
    

## 프로필 조회
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_profile = get_object_or_404(UserProfile, user=request.user)
        serializer = UserProfileSerializer(user_profile)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        #현재 인증된 사용자의 정보를 기반으로 객체를 조회
        #UserProfile 모델에서 user 필드가 현재 요청을 보낸 사용자와 일치하는 객체를 조회
        user_profile = get_object_or_404(UserProfile, user=request.user)
        serializer = UserProfileSerializer(user_profile, data=request.data, partial=True) #부분적 수정 기능
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

##친구추가
class AddFriendView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        email = request.data.get('email')
        #print('----여기까지 들어옵니다.----')#test
        
        try:
            friend = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"detail": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)

        user_profile = UserProfile.objects.get(user=request.user)
        user_profile.friends.add(friend)  # 이 부분은 UserProfile 모델에 friends 필드가 있는 것을 전제로 함

        return Response({"message": f"{friend.email}님을 친구로 추가했습니다."})


## 친구 목록 조회
class UserFriendView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # 현재 로그인한 사용자의 UserProfile 인스턴스를 가져옵니다.
        user_profile = get_object_or_404(UserProfile, user=request.user)
        # 해당 사용자의 친구 목록을 가져옵니다.
        friends = user_profile.friends.all()
        # 친구 목록을 serialize 합니다.
        serializer = UserFriendSerializer(friends, many=True)
        return Response(serializer.data)


##친구 프로필 조회
class FriendProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, friend_id):
        friend_profile = get_object_or_404(UserProfile, user_id=friend_id)

        # 해당 사용자의 프로필이 비공개이면서 요청한 사용자와 친구 관계가 아닐 경우
        if friend_profile.is_private and request.user not in friend_profile.friends.all():
            return Response({"message": "This account is private."}, status=status.HTTP_403_FORBIDDEN)

        serializer = UserProfileSerializer(friend_profile)
        return Response(serializer.data)


##친구삭제
class DeleteFriendView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        email = request.data.get('email')
        
        try:
            friend = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"detail": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)

        user_profile = UserProfile.objects.get(user=request.user)
        
        # 친구 목록에 해당 사용자가 있는지 확인
        if friend not in user_profile.friends.all():
            return Response({"detail": f"{friend.email}님은 친구 목록에 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

        user_profile.friends.remove(friend)  # 친구를 삭제

        return Response({"message": f"{friend.email}님을 친구 목록에서 삭제했습니다."})
    

## 친구 검색기능
class SearchFriendsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        keyword = request.query_params.get('keyword', '')

        # 이메일에 키워드가 포함된 사용자들 검색
        users = User.objects.filter(email__icontains=keyword)
        serializer = UserSerializer(users, many=True)
        
        return Response(serializer.data)

