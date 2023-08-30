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

    def put(self, request):
        user_profile = get_object_or_404(UserProfile, user=request.user)
        serializer = UserProfileSerializer(user_profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)