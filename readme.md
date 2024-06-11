

# Hyobot

Redmine에서 새로운 일감이 생성될 경우 할당된 사용자에게  카카오Work로 알림을 보낼 수 있도록 하는 미들웨어입니다.
효봇은 제 친구를 위해서 만들었습니다. 프로젝트 이름이 효봇인 이유는 친구 이름에 "효"자가 들어가서 그렇습니다.

레드마인에 다음의 플러그인을 설치하고 webhook url에 서버 url을 넣어주면 카카오톡으로 알림을 받을 수 있습니다.
https://github.com/suer/redmine_webhook


# 기능
포멧에 맞게 메시지를 보내면, 해당 메시지를 카카오톡으로 전송합니다.

# 설치 전 준비사항
- Windows 10 또는 그 이상 PC 또는 서버
- 인터넷 연결
- 카카오워크 봇 API Key 
  - 봇 생성방법은 문서를 참고: https://docs.kakaoi.ai/kakao_work/botdevguide/process/#bot-%EC%83%9D%EC%84%B1

# 사용되는 테크놀로지
대충 아래의 테크놀로지를 기반으로 Hyobot이 실행됩니다.
- [Docker](https://www.docker.com/)
- [WSL](https://learn.microsoft.com/ko-kr/windows/wsl/install) 
- [Git](https://git-scm.com/)
- [Python](https://www.python.org/)
- [FastAPI](https://fastapi.tiangolo.com/)

# 설치
본 설치 가이드는 리눅스는 무조건 어렵고 윈도우만 사용할 줄 아는 친구를 위해 아무것도 몰라도 완전히 처음부터 시작할 수 있도록 작성되었습니다. 최대한 쉬운 단어를 사용하고 단축어가 있다면 풀어쓰려고 노력하였으나 제 노력이 쓸모없을지도 모릅니다.

설치 단계는 다음과 같습니다.

1. 설치전 환경설정
2. 소스코드 복사
3. 서비스 환경설정
4. 도커 빌드 및 실행
5. API 문서 확인

## 1. 설치 전 환경설정
본 미들웨어를 실행하기 위해 필요한 환경을 구성하는 작업입니다.

### 1-1. WSL 설치
WSL은 Windows Subsystem for Linux로 윈도우 환경안에 가상의 리눅스 콤퓨타를 생성하는 작업입니다.
Windows 10 1904 이상에서 동작하며 본문에서는 WSL2 를 사용할 예정입니다. 

1. `시작` > `실행` > `명령 프롬프트` 를 선택하여 윈도우 터미널을 실행합니다.

2. 화면에 아래 명령어를 입력하여 wsl을 설치합니다. 인터넷 속도와 PC의 환경에 따라 다르지만 약 5분정도 소요됩니다.
    ```powershell 
    wsl --install
    ```
3. 설치중 id와 password를 입력하는데 이것은 꼭 기억해야 합니다. 나중에 다시 사용하게 됩니다.

5. WSL 설치가 완료되면 PC를 **재부팅**해야합니다.

### 1-2. Docker Desktop설치
Docker는 복잡한 설치환경을 손쉽게 구성해줄 수 있는 LXC(Linux Container)의 관리자의 한 종류입니다. 우리가 설치할 Docker Desktop은 이러한 Docker Engine설치와 구성, 모니터링을 UI로 할 수 있는 패키지 입니다.

[Docker 홈페이지](https://docs.docker.com/get-docker/)로 가서 Windows 용 Docker를 다운로드 후 설치파일을 실행합니다.

[https://docs.docker.com/get-docker/](https://docs.docker.com/get-docker/)

### 1-3. Docker 설정
도커가 실행되면 도커 데스크톱 어플리케이션 우측 상단의 `톱니바퀴`를 눌러서 설정으로 진입 후
`Resources` > `WSL Integration`으로 이동 후 방금 설치한 Ubuntu-22.04를 Switch ON 합니다.
이로서 WSL 내부에서 도커 명령을 실행할 수 있습니다.

### 1-4. WSL내에서 환경설정
시작 프로그램에서 `Ubuntu`를 실행하여 우분투 WSL 터미널을 엽니다.
아래 명령은 모두 WSL 환경안에서 실행합니다. Ubuntu 22.04 이상을 기준으로 작성되었습니다.

1. 먼저 패키지 목록을 업데이트 합니다. 패스워드를 물어보면 [1. WSL설치](#1.%20WSL%20%EC%84%A4%EC%B9%98) 에서 입력한 패스워드를 입력합니다.
    ```bash
    sudo apt update
    ```

2. 필요한 패키지들 (`make`, `pipx`)를 설치합니다.
    ```bash
    sudo apt install make pipx
    ```

3. pipx를 실행할 수 있도록 path를 조정합니다. 이 작업은 터미널 재시작이 필요합니다.
    ```bash
    pipx ensurepath
    ```

4. `exit`를 치면 터미널 창이 꺼집니다. 
    ``` bash
    exit
    ```

5. 다시한번 `시작`> `Ubuntu` 를 실행하여 터미널 창을 열어 poetry를 설치합니다.
    ```bash
    pipx install poetry
    ```

이로서 패키지를 실행할 수 있는 환경이 모두 설정되었습니다.

## 2. 소스코드 복사하기
소스코드를 자신의 디렉토리로 복사합니다.
```bash
git clone https://github.com/1kko/hyobot.git
```

## 3. 서비스 환경설정
`.env` 파일을 `hyobot` 디렉토리에 생성하고 아래에 카카오워크 봇 API 입력하는 단계입니다.
주의: 따움표나 스페이스를 제외하고 입력해주세요.

1. 복사한 폴더로 이동합니다.
    ```bash
    cd hyobot
    ```

2. `.env` 파일을 생성합니다.
    ```bash
    cat > .env << EOF
    APP_KEY=카카오.봇키1234abcd0000...
    EOF
    ```
3. `.env`파일의 내용을 확인합니다.
아래 내용이 생성했을 때 APP_KEY의 내용이 위의 입력값과 같으면 정상적으로 키가 입력된 것입니다. 참고로 `EOF`는 안보이는것이 정상입니다.
    ```bash
    cat .env
    ```

## 4. 도커 빌드 및 서비스 실행
도커를 빌드 (`make`) 하고  실행 (`make serve`) 합니다.
아래 명령어를 실행합니다
```bash
make && make serve
```

실행 후 윈도우 방화벽 알림이 오면 `허용` 해야만 사용이 가능합니다.


## 5. API 문서 확인
웹브라우저를 이용해서 `http://127.0.0.1:8000/docs` 접속이 되면 모든 것이 정상적으로 동작하는 것을 확인할 수 있습니다.

# Redmine 연동
1. 아래 홈페이지를 참조하여 레드마인에 플러그인을 설치하세요
https://github.com/suer/redmine_webhook

2. redmind 설정과 프로젝트 설정에서 webhook을 활성화 후 url을 다음과 같이 입력합니다.
    ```
    http://127.0.0.1:8000/new_message
    ```
여기서 `127.0.0.1`는 redmine과 hyobot이 동일한 서버에 설치되었을 경우이며, 다른 서버에 설치하였을 경우 해당 서버의 IP로 설정해야합니다.


## 6. 새로운 버전 업데이트 방법
1. 도커 데스크톱에서 현재 실행중인 hyobot을 멈춥니다.

2. 시작 프로그램에서 `Ubuntu`를 실행하여 우분투 WSL 터미널을 엽니다.

3. 아래 명령어를 입력합니다. 
```bash
cd hyobot
make && make serve
```

# 기타 주의사항
본 서비스는 모든 요청을 받을 수 있도록 오픈되어 있으므로 사용시 각별한 주의가 필요합니다. redmine 및 본 미들웨어 또한 인트라넷에서 사용하는 것을 가정하였으므로 보안에 관련된 조치는 아무것도 없습니다.
이러한 보안조치가 필요할 경우 소스코드 수정 또는 네트워크 설정을 통해 수신받는 IP를 제한하는등의 조치가 필요합니다.

# Reference

## Kakao Work API

https://docs.kakaoi.ai/kakao_work/webapireference/messages/


## POST API 포멧

Hyobot의 API(`127.0.0.1:8000/new_message`)에 `POST` 를 보낼 때에는 다음의 포멧으로 보내야 합니다.
전적으로 https://github.com/suer/redmine_webhook 의 데이터를 복제하였습니다.


### 새로운 일감 생성시
```json
{
  "payload": {
    "issue": {
      "author": {
        "icon_url": "http://www.gravatar.com/avatar/example",
        "identity_url": null,
        "lastname": "user",
        "firstname": "test",
        "mail": "test@example.com",
        "login": "test",
        "id": 3
      },
      "assignee": {
        "icon_url": "http://www.gravatar.com/avatar/example",
        "identity_url": null,
        "lastname": "user",
        "firstname": "test",
        "mail": "test@example.com",
        "login": "test",
        "id": 3
      },
      "priority": {
        "name": "normal",
        "id": 2
      },
      "tracker": {
        "name": "bug",
        "id": 1
      },
      "parent_id": null,
      "root_id": 191,
      "closed_on": null,
      "updated_on": "2014-03-01T15:17:48Z",
      "created_on": "2014-03-01T15:17:48Z",
      "description": "I'm having a problem with this.",
      "subject": "Found a bug",
      "id": 191,
      "done_ratio": 0,
      "start_date": "2014-03-02",
      "due_date": null,
      "estimated_hours": null,
      "is_private": false,
      "lock_version": 0,
      "project": {
        "homepage": "",
        "created_on": "2013-01-12T11:50:26Z",
        "description": "",
        "name": "Test Project",
        "identifier": "test",
        "id": 4
      },
      "status": {
        "name": "new",
        "id": 1
      }
    },
    "action": "opened",
    "url": "https://example.com"
  }
}
```

### 일감이 업데이트 되었을 경우
```json
{
  "payload": {
    "url": "https://example.com",
    "journal": {
      "details": [],
      "author": {
        "icon_url": "http://www.gravatar.com/avatar/example",
        "identity_url": null,
        "lastname": "user",
        "firstname": "test",
        "mail": "test@example.com",
        "login": "test",
        "id": 3
      },
      "assignee": {
        "icon_url": "http://www.gravatar.com/avatar/example",
        "identity_url": null,
        "lastname": "user",
        "firstname": "test",
        "mail": "test@example.com",
        "login": "test",
        "id": 3
      },
      "private_notes": false,
      "created_on": "2014-03-01T16:22:46Z",
      "notes": "Fixed",
      "id": 195
    },
    "issue": {
      "author": {
        "icon_url": "http://www.gravatar.com/avatar/example",
        "identity_url": null,
        "lastname": "user",
        "firstname": "test",
        "mail": "test@example.com",
        "login": "test",
        "id": 3
      },
      "priority": {
        "name": "normal",
        "id": 2
      },
      "tracker": {
        "name": "bug",
        "id": 1
      },
      "parent_id": null,
      "root_id": 196,
      "closed_on": null,
      "updated_on": "2014-03-01T16:22:46Z",
      "created_on": "2014-03-01T15:44:22Z",
      "description": "test",
      "subject": "Found a bug",
      "id": 196,
      "done_ratio": 0,
      "start_date": "2014-03-02",
      "due_date": null,
      "estimated_hours": null,
      "is_private": false,
      "lock_version": 2,
      "project": {
        "homepage": "",
        "created_on": "2013-01-12T11:50:26Z",
        "description": "",
        "name": "Test Project",
        "identifier": "test",
        "id": 4
      },
      "status": {
        "name": "normal",
        "id": 1
      }
    },
    "action": "updated"
  }
}
```
