from django.shortcuts import render
from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class TestJWTAuth(APIView):
    permission_classes = [IsAuthenticated]  # 이 view를 호출하기 위해서는 인증이 필요하다는 뜻 입니다(DRF 자체에서 아무나 들어올 수 없도록 막아주는 기본 기능입니다.)

    def get(self, request):
        user = request.user  # 현재 인증된 사용자 정보 가져오기
        return Response({"message": f"안녕하세요, {user}님! JWT인증이 완료되었습니다!."})