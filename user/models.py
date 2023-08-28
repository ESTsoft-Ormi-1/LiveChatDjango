from django.db import models

class CustomUser(models.Model):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    followers = models.ManyToManyField('self', blank=True, symmetrical=False)
    # 추가 필드 정의 가능
