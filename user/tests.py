# from django.test import TestCase

import requests

# 로그인 요청
login_url = "http://127.0.0.1:8000/login/"
data = {
    "username": "gony",
    "password": "qlalfqjsgh123"
}
response = requests.post(login_url, data=data)

# 응답 데이터 출력
print(response.status_code)
print(response.json().get("access"))  # 토큰은 response.json().get("access")로 추출 가능
