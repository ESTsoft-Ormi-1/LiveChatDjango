# LiveChatDjango
Django와 Channels를 활용하여 구축한 실시간 채팅 어플리케이션입니다.
# 프로젝트 일정 관리
https://www.notion.so/sungbinlee/e177dd0169e24b34826149a405e5a21d?pvs=4 
# ERD
![cobraspace_db](https://github.com/ESTsoft-Ormi-1/LiveChatDjango/assets/52542229/81a4b38d-0903-4d53-be10-1902e5aaa2d8)
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
# Fork 하기
