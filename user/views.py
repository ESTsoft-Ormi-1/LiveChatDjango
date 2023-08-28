# user/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import logout
from .models import CustomUser
from .serializers import CustomUserSerializer
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['user_id'] = self.user.id
        data['username'] = self.user.username
        data['email'] = self.user.email
        # 원하는 추가 정보를 토큰에 추가할 수 있습니다.
        return data

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class LogoutUserView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get('refresh_token')
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
                logout(request)  # 로그아웃 처리
                return Response({'message': '로그아웃되었습니다.'}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'message': '로그아웃 중 오류가 발생했습니다.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': '리프레시 토큰을 제공해주세요.'}, status=status.HTTP_400_BAD_REQUEST)

class FollowUserView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        user_to_follow = get_object_or_404(CustomUser, pk=user_id)
        if request.user != user_to_follow:
            request.user.followers.add(user_to_follow)
            return Response({'message': f'{user_to_follow.username}을(를) 팔로우했습니다.'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': '자기 자신을 팔로우할 수 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)

class UnfollowUserView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, user_id):
        user_to_unfollow = get_object_or_404(CustomUser, pk=user_id)
        if request.user != user_to_unfollow:
            request.user.followers.remove(user_to_unfollow)
            return Response({'message': f'{user_to_unfollow.username}을(를) 언팔로우했습니다.'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': '자기 자신을 언팔로우할 수 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)

class UpdateProfileView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request):
        serializer = CustomUserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterUserView(APIView):
    http_method_names = ['post']  # Only allow POST requests

    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
