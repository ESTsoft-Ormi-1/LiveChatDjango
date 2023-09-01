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

````
# Fork 하기
# SRS
# API 문서화
# API 앤드포인트(요청, 응답)
1. chat
```각자 api 나눠서 작성```
2. user
```각자 api 나눠서 작성```
3. post
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

```

```
````
