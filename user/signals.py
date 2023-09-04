
from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from .models import UserProfile

@receiver(user_signed_up)
def create_user_profile(sender, request, user, **kwargs):
    UserProfile.objects.create(user=user)
    # 회원가입 시에 프로필을 생성하는 시그널 리시버를 정의

