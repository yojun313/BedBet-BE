# BedBet-BE
2025 IST-TECH IT ARENA Hackathon BE

## API 명세서
모든 Endpoint 앞에
https://bedbet.knpu.re.kr/api/
Auth API 제외 API Request에 Bearer token `access_token` 설정 필요

## Auth

1. 로그인

**`POST` auth/signin**

- BODY

```json
{
		"email": "moonyojun@naver.com",
		"password": "abcd1234!"
}
```

- RESPONSE `200`

```json
{
    "message": "Token is valid",
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Im1vb255b2p1bkBuYXZlci5jb20ifQ.EpqWWXD_3xbu1h1BYFRZZBxVYjIzEeNGkYDUpt6EtZc",
    "user": {
        "email": "moonyojun@naver.com",
        "account_number": "1234",
        "bank": "우리은행",
        "coin": 0,
        "name": "문요준",
        "userUid": "16e14c74-14da-4180-8b81-e9db9d2704c3"
    }
}
```

- RESPONSE `400`

```json
{
		"message": "Incorrect password"
}
```

- RESPONSE `404`

```json
{
		"message": "User not found"
}
```

1. 토큰으로 로그인

**`POST` auth/signin/token**

- RESPONSE `200`

```json
{
		"message": "Token is valid",
		"user": {
        "email": "moonyojun@naver.com",
        "account_number": "1234",
        "bank": "우리은행",
        "coin": 0,
        "name": "문요준",
        "userUid": "16e14c74-14da-4180-8b81-e9db9d2704c3"
    }
}
```

- RESPONSE `404`

```json
{
		"message": "User not found"
}
```

1. 회원가입

**`POST` auth/signup**

- BODY

```json
{
    "email": "moonyojun@naver.com",
    "name": "문요준",
    "password": "abcd1234!",
    "account_number": "1234",
    "bank": "우리은행"
}
```

- RESPONSE `200`

```json
{
    "message": "User signed up successfully",
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Im1vb255b2p1bkBuYXZlci5jb20ifQ.EpqWWXD_3xbu1h1BYFRZZBxVYjIzEeNGkYDUpt6EtZc"
}
```

- RESPONSE `404`

```json
{
		"message": "Email not verified"
}
```

1. 이메일 인증 요청

**`POST` auth/verify/request**

- BODY

```json
{
	"email": "emample@example.com"
}
```

- RESPONSE `200`

```json
{
	"message": "Verification code sent"
}
```

1. 이메일 코드 인증

**`POST` auth/verify/email**

- BODY

```json
{
    "email": "moonyojun@naver.com",
    "code": "123456"
}
```

- RESPONSE `200`

```json
{
    "message": "Email verified successfully"
}
```

- RESPONSE `404`

```json
{
		"message": "Email not Found"
}
```

- RESPONSE `400`

```json
{
		"message": "Invalid verification code"
}
```

### Coin

1. 코인 요청하기

`post` coin/request

- BODY

```json
{
  "amount": 100
}
```

- RESPONSE `400` - **이미 코인 요청이 존재하는 경우**

```json
{
  "message": "Coin request already exists"
}
```

- RESPONSE `404` - **유저를 찾을 수 없는 경우**

```json
{
  "message": "User not found"
}
```

- RESPONSE `200` - **정상적으로 코인 요청이 제출된 경우**

```json
{
  "message": "Coin request submitted successfully"
}
```

1. 코인 요청 취소하기

`delete` coin/request/cancel

- RESPONSE `404` - **취소할 코인 요청이 존재하지 않는 경우**

```json
{
  "message": "No coin request found to cancel"
}
```

- RESPONSE `200` - **정상적으로 코인 요청이 취소된 경우**

```json
{
  "message": "Coin request cancelled successfully"
}
```

### Money

1. 출금 요청하기

`post` coin/request

- BODY

```json
{
  "amount": 11000
}
```

- RESPONSE `400` - **이미 출금 요청이 존재하는 경우**

```json
{
  "message": "Money request already exists"
}
```

- RESPONSE `404` - **유저를 찾을 수 없는 경우**

```json
{
  "message": "User not found"
}
```

- RESPONSE `400` - **유저의 코인이 부족한 경우**

```json
{
  "message": "Not enough coins to request money"
}
```

- RESPONSE `200` - **정상적으로 출금 요청이 제출된 경우**

```json
{
  "message": "Money request submitted successfully"
}
```

1. 출금 요청 취소하기

`delete` coin/request/cancel

- RESPONSE `404` - **취소할 출금 요청이 존재하지 않는 경우**

```json
{
  "message": "No money request found to cancel"
}
```

- RESPONSE `200` - **정상적으로 출금 요청이 취소된 경우**

```json
{
  "message": "Money request cancelled successfully"
}
```

## Team

1. 팀 목록 불러오기

`post` team/list

- RESPONSE `201`

```json
{
    "status_code": 201,
    "message": "Get teams success",
    "teams": [
        {
            "name": "팀이름1",
            "teamUid": "6a1680c8-244a-49d0-b75d-12e8557e2b31",
            "ownerUid": "16e14c74-14da-4180-8b81-e9db9d2704c1",
            "challenge_start_at": "2025-11-10T00:00:00",
            "challenge_end_at": "2025-11-10T01:30:00",
            "created_at": "2025-11-08T18:54:37.723000",
            "teammates": [
                {
                    "userUid": "16e14c74-14da-4180-8b81-e9db9d2704c3",
                    "coin": 100
                }
            ],
            "bet_coins": 100
        },
        {
            "name": "팀이름2",
            "teamUid": "6a1680c8-244a-49d0-b75d-12e8557e2b32",
            "ownerUid": "16e14c74-14da-4180-8b81-e9db9d2704c3",
            "challenge_start_at": "2025-11-10T00:00:00",
            "challenge_end_at": "2025-11-10T01:30:00",
            "created_at": "2025-11-08T18:54:37.723000",
            "teammates": [
                {
                    "userUid": "16e14c74-14da-4180-8b81-e9db9d2704c3",
                    "coin": 100
                }
            ],
            "bet_coins": 100
        }
    ]
}
```

1. 팀 만들기

`post` team/create

- BODY

```json
{
		"name": "team1",
		"challenge_start_at": "2025-11-10T00:00:00.000+00:00",
    "challenge_end_at": "2025-11-10T01:30:00.000+00:00",
    "coin": 100
}
```

- RESPONSE `400` - `challenge_start_at` 또는 `challenge_end_at`이 datetime 타입이 아님

```json
{
  "detail": {
    "message": "challenge_start_at and challenge_end_at must be datetime."
  }
}
```

- RESPONSE `400` - **시작/종료 시간이 KST 30분 단위로 정렬되지 않음**

```json
{
  "detail": {
    "message": "Start and end must be aligned to 30-minute boundaries in KST."
  }
}
```

- RESPONSE `400` - `challenge_start_at`이 `challenge_end_at`보다 같거나 늦은 경우

```json
{
  "detail": {
    "message": "challenge_start_at must be before challenge_end_at."
  }
}
```

- RESPONSE `400` - 사용자의 코인이 부족한 경우

```json
{
  "detail": {
    "message": "Insufficient coins to create the team."
  }
}
```

- RESPONSE `404` - 사용자를 찾을 수 없는 경우

```json
{
  "detail": {
    "message": "User not found."
  }
}
```

- RESPONSE `409` - 해당 사용자가 이미 팀을 소유하고 있는 경우

```json
{
  "detail": {
    "message": "This user already owns a team."
  }
}
```

- RESPONSE `409`- **동일한 팀 이름이 이미 존재하는 경우**

```json
{
  "detail": {
    "message": "Team name already exists."
  }
}
```

- RESPONSE `409` - **동일한 시작/종료 시간이 존재하는 팀이 이미 있을 경우**

```json
{
  "detail": {
    "message": "A team with the same start and end time already exists."
  }
}
```

1. 팀 가입하기

`post` team/join

- BODY

```json
{
  "teamUid": "e3a4b6c8-7d29-4c3b-a918-7a23d3d04e9e",
  "coin": 100
}

```

- RESPONSE `404` - **팀을 찾을 수 없는 경우**

```json
{
  "detail": {
    "message": "Team not found."
  }
}
```

- RESPONSE `409` - **해당 유저가 이미 팀 멤버인 경우**

```json
{
  "detail": {
    "message": "User already a member of the team."
  }
}
```

- RESPONSE `404` - **유저를 찾을 수 없는 경우**

```json
{
  "detail": {
    "message": "User not found."
  }
}
```

- RESPONSE `400` - **유저가 이미 다른 팀에 속해 있는 경우**

```json
{
  "detail": {
    "message": "User already belongs to a team."
  }
}
```

- RESPONSE `400` - **유저의 코인이 부족한 경우**

```json
{
  "detail": {
    "message": "Insufficient coins to join the team."
  }
}
```

- RESPONSE `200` - **정상적으로 팀에 가입한 경우**

```json
{
  "message": "Successfully joined team"
}
```

1. 팀 나가기

`post` team/exit

- BODY

```json
{
  "teamUid": "e3a4b6c8-7d29-4c3b-a918-7a23d3d04e9e"
}
```

- RESPONSE `404` - **팀을 찾을 수 없는 경우**

```json
{
  "detail": {
    "message": "Team not found."
  }
}
```

- RESPONSE `400` - **해당 유저가 팀 멤버가 아닌 경우**

```json
{
  "detail": {
    "message": "User is not a member of the team."
  }
}
```

- RESPONSE `500` - **DB에 잘못된 challenge_start_at 값이 존재하는 경우**

```json
{
  "detail": {
    "message": "Invalid challenge_start_at in DB."
  }
}
```

- RESPONSE `400` - **챌린지가 이미 시작된 이후에 팀을 나가려는 경우**

```json
{
  "detail": {
    "message": "Cannot exit team after challenge has started."
  }
}
```

- RESPONSE `200` - **정상적으로 팀을 나간 경우**

```json
{
  "message": "Successfully exited the team."
}
```

1. 팀 정보 조회

`get` team/info/{teamUid}

- RESPONSE `404` - **팀을 찾을 수 없는 경우**

```json
{
  "detail": {
    "message": "Team not found."
  }
}
```

- RESPONSE `200` - **정상적으로 팀 정보를 조회한 경우**

```json
{
  "message": "Get team info success",
  "team": {
    "teamUid": "e3a4b6c8-7d29-4c3b-a918-7a23d3d04e9e",
    "name": "team1",
    "ownerUid": "1f9a6d3b-5e91-4f63-aabc-9d6d2e10b4e2",
    "challenge_start_at": "2025-11-10T00:00:00.000Z",
    "challenge_end_at": "2025-11-10T01:30:00.000Z",
    "created_at": "2025-11-08T07:30:00.000Z",
    "teammates": [
      { "userUid": "1f9a6d3b-5e91-4f63-aabc-9d6d2e10b4e2", "coin": 100 },
      { "userUid": "4f2a8a1b-6d2e-4d51-9e2f-23b7a91f1d33", "coin": 150 }
    ],
    "bet_coins": 250
  }
}
```

1. 유저 팀 탈락 처리

`get` team/disqualify

- RESPONSE `404` - **유저를 찾을 수 없는 경우**

```json
{
  "detail": {
    "message": "User not found."
  }
}
```

- RESPONSE `404` - **팀을 찾을 수 없는 경우**

```json
{
  "detail": {
    "message": "Team not found."
  }
}
```

- RESPONSE `400` - **유저가 팀 멤버가 아닌 경우**

```json
{
  "detail": {
    "message": "User is not a member of the team."
  }
}
```

- RESPONSE `200` - **정상적으로 유저가 탈락 처리된 경우**

```json
{
  "message": "User has been disqualified and removed from the team.",
  "lost_coins": 100
}
```

### User

1. 사용자 정보 조회

`get` user/info

- RESPONSE `200` - **정상적으로 사용자 정보를 조회한 경우**

```json
{
  "user": {
    "userUid": "16e14c74-14da-4180-8b81-e9db9d2704c3",
    "email": "yojun313@postech.ac.kr",
    "name": "문요준",
    "account_number": "1234",
    "coin": 500,
    "teamUid": "e3a4b6c8-7d29-4c3b-a918-7a23d3d04e9e",
    "createdAt": "2025-11-01T05:00:00.000Z",
    "updatedAt": "2025-11-08T06:30:00.000Z"
  }
}
```

- RESPONSE `404` - **유저를 찾을 수 없는 경우**

```json
{
  "message": "User not found"
}
```

1. 사용자 탈퇴

`delete` /

- RESPONSE `200` - **정상적으로 사용자가 삭제된 경우**

```json
{
  "message": "User deleted successfully"
}
```