```# LiveChatDjango
Django와 Channels를 활용하여 구축한 실시간 채팅 어플리케이션입니다.
# 프로젝트 일정 관리
https://www.notion.so/sungbinlee/e177dd0169e24b34826149a405e5a21d?pvs=4
# ERD
![1-1](https://github.co
m/ESTsoft-Ormi-1/LiveChatDjango/assets/52542229/b2190861-6e89-4809-9d19-7e7d442b98e2)
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
source venv/bin/activate # Windows에서는 "venv\Scripts\activate" 실행
pip install -r requirements.txt

```

4. migrate
```

python manage.py migrate

```

5. 개발 서버 실행
```

python manage.py runserver

# Fork 하기
# SRS
# API 문서화
# API 앤드포인트(요청, 응답)
## 1. chat
```각자 api 나눠서 작성```
## 2. user
### 2-1 회원가입
---
* URL: /user/registration/
* Method: POST
* Description: 사용자의 정보를 사용하여 회원가입을 진행합니다.
---
**요청:**
```python
{
    "email": "이메일 주소",
    "password": "비밀번호",
    ...
}
```
**응답:**
```python
{
    "email": "이메일 주소",
    "message": "회원가입이 완료되었습니다.",
    "profile": {
        ...  # 프로필 정보
    }
}
```
---
* 회원가입된 이메일 입력시
```python
응답 :
{
    "email": [
        "A user is already registered with this e-mail address."
    ]
}
```

### 2-2 로그인
---
* URL: /user/login/
* Method: POST
* Description: 사용자의 이메일과 비밀번호를 사용하여 로그인을 진행합니다.
---
**요청:**
```python

{
    "email": "이메일 주소",
    "password": "비밀번호"
}
```
---
**응답:**
```python
{
    "message": "환영합니다.",
    "profile": {
        ...  # 프로필 정보
    },
    "refresh": "JWT Refresh 토큰",
    "access": "JWT Access 토큰"
}
```
### 2-3 로그아웃
---
* URL: /user/logout/
* Method: POST
* Description: 로그아웃을 진행합니다.
---
**응답:**
```python
{
    "message": "로그아웃이 완료되었습니다."
}
```

### 2-4 친구추가(jwt)
---
* URL: /user/add-friend/
* Method: POST
* Description: 인증된 사용자 접근시 친구를 추가합니다.
---
**요청:**
```python
{
    "email": "친구의 이메일 주소"
}
```
---
**응답:**
```python
{
    "message": "친구 추가 완료 메시지"
}
```
### 2-5 친구 목록 조회(jwt)
---
* URL: /user/friends/
* Method: GET
* Description: 인증된 사용자 접근시 친구 목록을 조회합니다.
---
**응답:**
```python
{
    ...  # 친구 목록 정보
}
```
### 2-6 친구(사용자) 프로필 조회
---
* URL: /user/friend-profile/<int:friend_id>/
* Method: GET
* Description: 인증된 사용자 접근시 특정 사용자의 프로필 정보를 조회합니다.
---
**응답:**
```python
{
    ...  # 친구의 프로필 정보
}
```
### 2-7 친구 검색
---
* URL: /user/search-friends/?keyword=[이메일 정보]
* Method: GET
* Description: 인증된 사용자 접근시 키워드를 기반으로 친구를 검색합니다.
---
**쿼리 파라미터**
```python
{
    "keyword": "검색할 키워드(이메일에 포함된 키워드)"
}
```
---
**응답:**
```python
{
    ...  # 검색된 사용자들의 정보
}
```
### 2-8 친구 삭제
---
* URL: /user/delete-friend/
* Method: POST
* Description: 인증된 사용자 접근시 친구목록에 친구 존재하면 친구를 삭제합니다.
---
**요청:**
```python
{
    "email": "삭제할 친구의 이메일 주소"
}
```
---
**응답:**
```python
{
    "message": "친구 삭제 완료 메시지"
}
```
---
* 친구목록에 없을 경우
**응답**
```python
{
    "detail": "user5@email.com님은 친구 목록에 없습니다."
}
```
## 3. post
### 게시물검색 (Post search)
- URL: api/post/categories
- Method: POST
- Description: 존재하는 모든 카테고리의 목록을 볼 수 있습니다.
- Request Body:
```json
{
    "id": 1,
    "name": "Programming"
},
{
    "id": 2,
    "name": "Ormi"
},
{
    "id": 3,
    "name": "ESTsoft"
}
```

### 게시물검색 (Post search)
- URL: api/post/?search=title
- Method: POST
- Description: 작성한 키워드에 해당하는 게시물의 목록을 볼 수 있습니다.
- Request Body:
```json
{
    "id": 2,
    "tags": [],
    "title": "Title2",
    "content": "content2",
    "created_at": "2023-08-30T16:46:04.899333+09:00",
    "updated_at": "2023-08-30T16:58:01.008073+09:00",
    "hit": 0,
    "category": 1
},
{
    "id": 3,
    "tags": [],
    "title": "New Post Title",
    "content": "This is the content of the new post.",
    "created_at": "2023-08-30T17:03:28.688333+09:00",
    "updated_at": "2023-08-30T17:03:28.688333+09:00",
    "hit": 0,
    "category": 1
}
```


# UI(구현 동작)

# 개발 이슈

# 각종 사용한 링크, 피그마?

# 후기
