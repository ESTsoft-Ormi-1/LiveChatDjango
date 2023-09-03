# 🐍 코브라 스페이스
**코브라 스페이스**는 코딩과 프로그래밍에 관한 주제로 된 **라이브 채팅 커뮤니티**입니다. 이 커뮤니티는 **코딩 열정가들**이 모여 정보를 공유하고 협력할 수 있는 플랫폼을 제공합니다.
<img width="1384" alt="image" src="https://github.com/ESTsoft-Ormi-1/LiveChatDjango/assets/52542229/882b5d47-1750-491d-a27f-a576fd8686c1">
### 코브라의 의미
> "코브라"는 "**COding BRAinstorm**"의 줄임말입니다.

코브라 스페이스는 코딩과 프로그래밍 분야에서 아이디어를 공유하고 협력하는 공간을 상징합니다. 개발자들의 지식 공유, 네트워킹, 그리고 협력을 촉진하는 역할을 하며, 커뮤니티 내에서 새로운 아이디어와 프로젝트의 탄생을 돕습니다.
### 프로젝트 기간
`2023.08.17 ~ 2023.09.04`
## 주요 기능
1. **게시글 기능**: 사용자들은 다양한 주제에 대한 게시글을 작성할 수 있습니다. 이 게시글은 **프로그래밍과 관련된 다양한 주제**를 다룰 수 있으며, 지식과 경험을 공유하고 질문을 할 수 있는 장을 제공합니다.

2. **유저 기능**: 사용자들은 개인 프로필을 만들고 자신의 **코딩 역량과 관심사**를 공유할 수 있습니다. 이를 통해 다른 사용자와 연결하고 커뮤니티 내에서 활발한 활동을 할 수 있습니다.

3. **채팅 기능**: 게시글의 주제에 따라 **채팅방에 참여**할 수 있습니다. 이렇게 하면 게시글 내용에 대한 토론을 더 쉽게 진행할 수 있으며, 사용자들은 **관심 있는 주제에 대한 논의**에 참여할 수 있습니다.


## 역할 분담

## SRS

## API
### 1. Chat
#### 1.1 메시지 관리
##### 1.1.1 메세지 생성
* URL: `/api/chat/message/`
* Method: POST
* Description: 새로운 채팅 메세지를 생성합니다.

**요청 예시**:
```json
{
  "type": "chat.message",
  "message": "Hello, World!"
}
```
#### 1.2 방 관리
##### 1.2.1 방 생성
* URL: `/api/chat/room/`
* Method: POST
* Description: 새로운 대화방을 생성합니다.

**요청 예시**:
```json
{
  "name": "Chat Room"
}
```
##### 1.2.2 방 조회
* URL: `/api/chat/room/{room_id}/`
* Method: POST
* Description: 특정 대화방을 조회합니다.
* 요청 파라미터: `{room_id}` - 조회할 방의 고유 식별자

**요청 예시**:
```json
{
  "id": 42,
  "name": "Chat Room",
  "chat_url": "/ws/chat/42/chat/"
}
```
#### 1.3 Websocket 
##### 1.3.1 Websocket 연결
* URL: `wss://example/ws/chat/{room_id}/chat/`
* Description: 클라이언트는 이 엔드포인트를 통해 웹소켓 서버에 연결할 수 있습니다.
##### 1.3.2 메시지 교환
##### 메시지 유형:
WebSocket 연결을 통해 주고받는 메시지는 다음과 같은 유형을 가질 수 있습니다:
* `chat.message`: 일반 채팅 메시지
* `chat.user.join`: 사용자가 채팅방에 입장한 이벤트
* `chat.user.leave`: 사용자가 채팅방에서 퇴장한 이벤트
##### 메시지 전송:
클라이언트는 JSON 형식의 메시지를 WebSocket 서버로 전송할 수 있습니다. 메시지의 형식은 다음과 같습니다:
```json
{
  "type": "chat.message",
  "message": "Hello, World!"
}
```
##### 메시지 수신:
WebSocket 서버는 다른 클라이언트로부터 수신한 메시지를 현재 연결된 클라이언트에게 전달합니다.
```json
{
  "type": "chat.message",
  "message": "Hello, World!",
  "sender": "user@example.com",
  "nickname": "John",
  "profile_picture_url": "https://example.com/profile.jpg"
}
```
##### 이벤트 처리:
클라이언트는 chat.user.join 및 chat.user.leave 이벤트를 수신하여 사용자의 입장 및 퇴장을 처리할 수 있습니다.
```json
{
  "type": "chat.user.join",
  "username": "John"
}
```
##### 오류 처리
WebSocket API에서 오류가 발생할 경우, 클라이언트는 적절한 오류 메시지를 수신합니다. 오류 메시지의 형식은 다음과 같습니다:
```json
{
  "error_type": "invalid_request",
  "message": "Invalid message format."
}
```
### 2. user
#### 2.1 회원가입
* URL: `/api/user/registration/`
* Method: POST
* Description: 사용자의 정보를 사용하여 회원가입을 진행합니다.
**요청:**
```json
{
    "email": "이메일 주소",
    "password": "비밀번호",
    ...
}
```
**응답:**
```json
{
    "email": "이메일 주소",
    "message": "회원가입이 완료되었습니다.",
    "profile": {
        ...  # 프로필 정보
    }
}
```
* 회원가입된 이메일 입력시
응답 :
```json
{
    "email": [
        "A user is already registered with this e-mail address."
    ]
}
```

### 2.2 로그인
* URL: `/api/user/login/`
* Method: POST
* Description: 사용자의 이메일과 비밀번호를 사용하여 로그인을 진행합니다.
**요청:**
```json

{
    "email": "이메일 주소",
    "password": "비밀번호"
}
```
**응답:**
```json
{
    "message": "환영합니다.",
    "profile": {
        ...  # 프로필 정보
    },
    "refresh": "JWT Refresh 토큰",
    "access": "JWT Access 토큰",
}
```
### 2.3 로그아웃
* URL: /user/logout/
* Method: POST
* Description: 로그아웃을 진행합니다.
**응답:**
```json
{
    "message": "로그아웃이 완료되었습니다."
}
```

### 2.4 친구추가
* URL: `/api/user/add-friend/`
* Method: POST
* Description: 인증된 사용자 접근시 친구를 추가합니다.
**요청:**
```python
{
    "email": "친구의 이메일 주소"
}
```
**응답:**
```python
{
    "message": "친구 추가 완료 메시지"
}
```
### 2.5 친구 목록 조회

* URL: `/api/user/friends/`
* Method: GET
* Description: 인증된 사용자 접근시 친구 목록을 조회합니다.
**응답:**
```python
{
    ...  # 친구 목록 정보
}
```
### 2.6 친구(사용자) 프로필 조회
* URL: `/api/user/friend-profile/<int:friend_id>/`
* Method: GET
* Description: 인증된 사용자 접근시 특정 사용자의 프로필 정보를 조회합니다.
**응답:**
```json
{
    ...  # 친구의 프로필 정보
}
```
### 2.7 친구 검색
* URL: `/api/user/search-friends/?keyword=[이메일 정보]`
* Method: GET
* Description: 인증된 사용자 접근시 키워드를 기반으로 친구를 검색합니다.
---
**쿼리 파라미터**
```json
{
    "keyword": "검색할 키워드(이메일에 포함된 키워드)"
}
```
---
**응답:**
```json
{
    ...  # 검색된 사용자들의 정보
}
```
### 2.8 친구 삭제
---
* URL: `/api/user/delete-friend/`
* Method: POST
* Description: 인증된 사용자 접근시 친구목록에 친구 존재하면 친구를 삭제합니다.
---
**요청:**
```json
{
    "email": "삭제할 친구의 이메일 주소"
}
```
---
**응답:**
```json
{
    "message": "친구 삭제 완료 메시지"
}
```
---
* 친구목록에 없을 경우
**응답**
```json
{
    "detail": "user5@email.com님은 친구 목록에 없습니다."
}
```
## 3. post
### 3.1 카테고리 검색
- URL: `api/post/categories`
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

### 3.2 게시물검색
- URL: `/api/post/?search=title`
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
## UI(구현 동작)

| 0. 로그인 & 로그아웃 |
|-----|
| ![ezgif-5-c781aa6d04](https://github.com/ESTsoft-Ormi-1/LiveChatDjango/assets/52542229/9c9f22ab-9e02-4fc6-9267-3910ecfba7fd) |

| 1. 프로필 조회 |
|-----|
| ![ezgif-3-7d31370f4c](https://github.com/ESTsoft-Ormi-1/LiveChatDjango/assets/52542229/4dedeb2e-8afa-47e5-9200-b9e722c5f852)|

| 2. 게시글 조회 |
|-----|
|  ![ezgif-5-eb629f9f12](https://github.com/ESTsoft-Ormi-1/LiveChatDjango/assets/52542229/31da3483-a8c5-4192-a35d-c40ac222391f)|

| 3. 채팅 기능 |
|-----|  
| <video src=https://github.com/ESTsoft-Ormi-1/LiveChatDjango/assets/52542229/411a3e26-d9c5-4538-952b-f821332323bd>  |

| 4. 게시글 작성 |
|-----|  
| <video src=https://github.com/ESTsoft-Ormi-1/LiveChatDjango/assets/52542229/2af01f92-833b-4941-9ea8-2f934bf797b9>  |
## 개발 이슈

## 각종 사용한 링크, 피그마?

## 후기
