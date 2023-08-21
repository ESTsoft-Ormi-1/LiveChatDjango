# LiveChatDjango
Django와 Channels를 활용하여 구축한 실시간 채팅 어플리케이션입니다.
# 프로젝트 일정 관리
https://www.notion.so/sungbinlee/e177dd0169e24b34826149a405e5a21d?pvs=4 
# ERD
![1-1](https://github.com/ESTsoft-Ormi-1/LiveChatDjango/assets/52542229/b2190861-6e89-4809-9d19-7e7d442b98e2)
# 시작하기
1. 이 레포지토리를 복사합니다.
```
git clone https://github.com/ESTsoft-Ormi-1/LiveChatDjango
```
2. 복사한 폴더로 들어가기
```
cd LiveChatDjango
```
3. 가상환경 생성
```
python -m venv venv
source venv/bin/activate  # Windows에서는 "venv\Scripts\activate" 실행
pip install -r requirements.txt
```

4. migrate
```
python manage.py migrate
```

5. 개발 서버 실행
```
python manage.py runserver
```
