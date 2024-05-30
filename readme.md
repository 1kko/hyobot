# Hyobot

효봇은 김정효를 위해서 만든 카카오 알림봇입니다.

## 기능
- 포멧에 맞게 메시지를 보내면, 해당 메시지를 카카오톡으로 전송합니다.

## 설치

### 0. 설치전 준비사항
- [Docker](https://docs.docker.com/get-docker/)
- amd64 또는 x86
- 인터넷 연결
- 카카오워크 봇 API Key

아래 명령은 모두 WSL 환경안에서 실행합니다. Ubuntu 22.04 이상을 기준으로 작성되었습니다.

### 1. 레포지토리 클론
```bash
git clone https://github.com/1kko/hyobot.git
```

### 2. `.env` 파일을 `hyobot` 디렉토리에 생성하고 아래에 카카오워크 봇 API 입력
주의: 따움표나 스페이스를 제외하고 입력해주세요.
```bash
APP_KEY=카카오.봇키1234abcd0000...
```

### 3. 도커 빌드
```bash
make
```

### 4. 실행
```
make serve
```

### 5. 웹브라우저를 이용해서 `https://127.0.0.1:8000/docs` 접속 후 payload에 맞추어 데이터를 post 하시면 됩니다.
