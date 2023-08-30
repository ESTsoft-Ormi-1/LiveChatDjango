from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView 
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import UserProfileSerializer
from .models import UserProfile, User
from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView, LogoutView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken


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
    

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_profile = get_object_or_404(UserProfile, user=request.user)
        serializer = UserProfileSerializer(user_profile)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        user_profile = get_object_or_404(UserProfile, user=request.user)
        serializer = UserProfileSerializer(user_profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

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


class FriendProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, friend_id):
        friend_profile = get_object_or_404(UserProfile, user_id=friend_id)
        serializer = UserProfileSerializer(friend_profile)
        return Response(serializer.data)