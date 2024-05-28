#!/usr/bin/env python3

"""
카카오 워크에 대한 API를 사용하는 모듈입니다.
Ref Doc: https://docs.kakaoi.ai/kakao_work/webapireference/messages/
제 친구 삽돌이를 위해 만들었습니다. 무단전제 재배포 무제한 가능. Copyleft 2024.

"""
import os
from urllib.parse import urljoin
import json

import requests
from dotenv import load_dotenv

load_dotenv()


class Client:
    """Define default restful api client for KakaoWork."""

    REQUEST_TIMEOUT = 10
    BASE_URL = "https://api.kakaowork.com/v1/"

    def __init__(self):
        self.HEADERS = {
            "Authorization": f"Bearer {os.getenv('APP_KEY')}",
            "Content-Type": "application/json;charset=utf-8",
        }

    def get(self, endpoint: str, params: dict = None):
        """
        Sends a GET request to the specified endpoint.

        Args:
            endpoint (str): The endpoint to send the request to.

        Returns:
            dict: The JSON response from the server, if the request is successful.

        Raises:
            Exception: If an error occurs while sending the request.
        """
        url = urljoin(self.BASE_URL, endpoint)
        try:
            response = requests.get(
                url, headers=self.HEADERS, params=params, timeout=self.REQUEST_TIMEOUT
            )
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            raise e

    def post(self, endpint: str, data: dict):
        """
        Sends a POST request to the specified endpoint with the given data.

        Args:
            endpoint (str): The endpoint to send the request to.
            data (dict): The data to include in the request payload.

        Returns:
            dict: The JSON response from the server, if the request is successful.

        Raises:
            Exception: If an error occurs while sending the request.
        """
        url = urljoin(self.BASE_URL, endpint)
        try:
            response = requests.post(
                url, headers=self.HEADERS, json=data, timeout=self.REQUEST_TIMEOUT
            )
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            raise e


class Endpoints:
    """Endpoints for KakaoWork API."""

    def __init__(self) -> None:
        self.client = Client()

    def spaces_info(self) -> dict:
        """워크스페이스의 정보를 조회합니다.

        Returns:
            dict: Information of the space.

        Return Example:
        _ = {
            "space": {
                "color_code": "default",
                "color_tone": "light",
                "id": 230021,
                "kakaoi_org_id": 285847,
                "logo_url": "",
                "name": "Rhaon Ent.",
                "permitted_ext": ["*"],
                "profile_name_format": "name_only",
                "profile_position_format": "responsibility",
            }
        }
        """
        endpoint = "spaces.info"
        return self.client.get(endpoint).get("space")

    def departments_list(self) -> list[dict]:
        """워크스페이스에 속한 전체 부서 정보를 조회합니다.

        Returns:
            list[dict]: Information of the departments.

        Return Example:
        _ = {
            "cursor": "Y3Vyc29yX2lkPTQ1NDkwMiZsaW1pdD0xMA==",
            "departments": [
                {
                    "ancestry": "",
                    "code": "d29ya3N............tMjMwMDIx",
                    "depth": 0,
                    "has_child": False,
                    "id": "400002",
                    "ids_path": "400002",
                    "leader_ids": [],
                    "name": "R Ent.",
                    "order": 0,
                    "parent_id": 0,
                    "space_id": "200001",
                    "user_count": 82,
                    "users_ids": [],
                },
                {
                    "ancestry": "4000062/400006/400003",
                    "code": "NBC01DQz",
                    "depth": 3,
                    "has_child": False,
                    "id": "400002",
                    "ids_path": "400002/400006/400003/400003",
                    "leader_ids": [10085396],
                    "name": "PM팀",
                    "order": 0,
                    "parent_id": 400003,
                    "space_id": "200001",
                    "user_count": 5,
                    "users_ids": [10080006, 10080005, 10006010, 10080001, 10050003],
                },
                ...
            ],
            "success": True,
        }

        """
        endpoint = "departments.list"
        # loop until cursor is None
        params = {}
        departments = []
        while True:
            response = self.client.get(endpoint, params)
            departments.extend(response.get("departments", []))

            cursor = response.get("cursor")
            if cursor is None:
                break

            params["cursor"] = cursor

        return departments

    def users_info(self, user_id: str | None = None, email: str | None = None) -> dict:
        """워크스페이스에 속한 특정 멤버의 상세 정보를 얻습니다.

        Response Example:
        _ = {
            "success": True,
            "user": {
                "avatar_url": "https://kagedn.kakaoicdn.net/dn/djTMNV/hyQdzDdu0P/ULQjzNE0eRNhUvB0/img_l.jpg",
                "department": "A팀",
                "display_name": "김삽효",
                "emails": [],
                "id": "10000003",
                "identifications": [{"type": "email", "value": "jeonghyo.kim@rent.co.kr"}],
                "mobiles": ["01012345678"],
                "name": "김삽효",
                "nickname": None,
                "position": None,
                "responsibility": "팀원",
                "space_id": "400002",
                "status": "activated",
                "tels": [],
                "vacation_end_time": None,
                "vacation_start_time": None,
                "work_end_time": None,
                "work_start_time": None,
            },
        },
        """

        if user_id is None and email is None:
            raise ValueError("user_id or email must be provided.")
        if user_id:
            endpoint = "users.info"
            params = {"user_id": user_id}
            return self.client.get(endpoint, params).get("user")
        if email:
            endpoint = "users.find_by_email"
            params = {"email": email}
            return self.client.get(endpoint, params).get("user")

    def conversations_open(self, user_id: str) -> dict:
        """특정 사용자와의 1:1 대화를 생성합니다.

        Args:
            user_id (str): 대화를 생성할 사용자의 ID

        Returns:
            dict: Response of the conversation opening.

        Return Example:
        _ = {
            "conversation_id": "1",
            "success": True,
        }
        """
        endpoint = "conversations.open"
        data = {"user_id": user_id}
        return self.client.post(endpoint, data).get("conversation")

    def send_message(
        self,
        text: str,
        conversation_id: str | None = None,
        blocks: str | None = None,
        email: str | None = None,
    ) -> json:
        """메시지를 전송합니다.

        Args:
            text (str): 전송할 채팅 메시지
                        - 일반 텍스트 메시지를 전달할 때 사용
                        - 메시지를 text 형식이 아닌 blocks로 정의했을 때, 푸시 알림과 채팅방 목록과 같이
                          조합형 말풍선 메시지가 사용될 수 없는 경우에 활용되는 대체(Fallback) 메시지
                        - 메시지 최대 길이는 3,000자 이하

            conversation_id (str): 메시지를 전송할 채팅방의 ID
            email (str): 메시지를 전송할 사용자의 이메일 주소 (conversation_id가 있을경우 무시됨)
            blocks (list[dict]): (optional) 조합형 말풍선 메시지를 전달할 때 사용
                        - Block Kit 구성 및 정책 문서 참고 https://blockkit.kakaowork.com/

        Request Example:
        _ = {
            "conversation_id": "1",
            "text": "카카오워크에 오신걸 환영합니다.",
            "blocks": [
                {
                    "type": "text",
                    "text": "카카오워크에 오신걸 환영합니다.",
                    "inlines": [
                        {"type": "styled", "text": "카카오워크에 "},
                        {"type": "styled", "text": "오신걸 ", "bold": true},
                        {"type": "styled", "text": " 환영합니다.", "color": "red"},
                    ],
                }
            ],
        }

        Returns:
            json: Response of the message sending.

        Return Example:
        _ = {
            "message_id": "5",
            "success": True,
        }
        """

        data = {
            "conversation_id": conversation_id,
            "email": email,
            "text": text,
            "blocks": blocks,
        }

        if blocks is None:
            data.pop("blocks")

        if conversation_id is None and email is None:
            raise ValueError("conversation_id or email must be provided.")

        if email is None:
            data.pop("email")

        if conversation_id is None:
            data.pop("conversation_id")

        if conversation_id:
            endpoint = "messages.send"
            return self.client.post(endpoint, data)

        if email:
            endpoint = "messages.send_by_email"
            return self.client.post(endpoint, data)


def main():
    """Main"""
    kwe = Endpoints()
    # space 정보
    print(kwe.spaces_info())

    print(kwe.departments_list())

    # 부서 정보
    departments = kwe.departments_list()
    print(departments)

    # 부서에 속한 유저 정보
    users = []
    for department in departments:
        user_ids = department.get("users_ids")
        for user_id in user_ids:
            user = kwe.users_info(user_id)
            users.append(user)
    print(users)

    # 사용자 ID 찾기
    user = kwe.users_info(email="kimjeonghyo@rhaon.co.kr")
    print(user)

    # 1:1 대화 생성
    conversation = kwe.conversations_open(user_id=user.get("id"))
    print(conversation)

    # 메시지 전송
    message = kwe.send_message(
        conversation_id=conversation.get("id"),
        text="안녕하세요. 저는 HyoBot입니다. 또봇 아니에영.",
    )
    print(message)

    msg = {
        "text": "새로운 이슈입니다.",
        "blocks": [
            {
                "type": "text",
                "text": "text sample",
                "inlines": [
                    {
                        "type": "styled",
                        "text": "결함 ",
                        "bold": True,
                        "color": "red",
                    },
                    {"type": "styled", "text": "[보통] "},
                    {"type": "styled", "text": "님아 제발좀 봐주셈"},
                ],
            },
            {
                "type": "button",
                "text": "헬게이트 열어보기",
                "style": "default",
                "action": {
                    "type": "open_system_browser",
                    "name": "button1",
                    "value": "http://google.com/search?q=헬게이트",
                },
            },
        ],
    }

    result = kwe.send_message(
        email="kimjeonghyo@rhaon.co.kr",
        text="새로운 이슈입니다.",
        blocks=msg.get("blocks"),
    )
    print(result)


if __name__ == "__main__":
    main()
