# Hyobot

효봇은 김정효를 위해서 만든 카카오 알림봇입니다.

## 기능
- 포멧에 맞게 메시지를 보내면, 해당 메시지를 카카오톡으로 전송합니다.

## 설치

### 0. 설치전 준비사항
- amd64 또는 x86
- 인터넷 연결
- 카카오워크 봇 API Key

1. WSL 설치
```
wsl --install
```
패스워드는 꼭 기억해야 합니다. 나중에 다시 사용합니다.
WSL 설치가 완료되면 PC를 재부팅해야합니다.

2. Docker 설치
- [Docker](https://docs.docker.com/get-docker/)
Docker로 가서 자신의 PC에 맞는 버전을 다운로드 후 설치파일을 실행합니다.

3. Docker 설정
도커가 실행되면 톱니바퀴를 눌러서 설정으로 진입 후
Resources > WSL Integration으로 이동후 방금 설치한 Ubuntu-22.04를 Switch ON 합니다.

4. WSL내에서 환경설정

아래 명령은 모두 WSL 환경안에서 실행합니다. Ubuntu 22.04 이상을 기준으로 작성되었습니다.

```bash
sudo apt update
sudo apt install make pipx
pipx ensurepath
exit
```
`exit`를 치면 터미널 창이 꺼집니다. 
시작 > Ubuntu 를 실행하여 터미널 창을 열어 poetry를 설치합니다.

```
pipx install poetry
```


### 1. 레포지토리 클론
```bash
git clone https://github.com/1kko/hyobot.git
```

### 2. `.env` 파일을 `hyobot` 디렉토리에 생성하고 아래에 카카오워크 봇 API 입력
주의: 따움표나 스페이스를 제외하고 입력해주세요.

1. 클론 받은 레포지토리로 이동합니다.
```bash
cd hyobot
```

2. `.env` 파일을 생성합니다.
```
cat > .env << EOF
APP_KEY=카카오.봇키1234abcd0000...
EOF
```
3. `.env`파일의 내용을 확인합니다.
```bash
cat .env
# APP_KEY=카카오.봇키1234abcd0000...
```

### 3. 도커 빌드
```bash
make
```

### 4. 실행
```
make serve
```

### 5. 웹브라우저를 이용해서 `http://127.0.0.1:8000/docs` 접속 후 payload에 맞추어 데이터를 post 하시면 됩니다.
