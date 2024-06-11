"""FastAPI Server which receives as POST and sends to kakaowork API"""

from typing import Any

from fastapi import Body, FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from kakaowork import Endpoints
from util import getDict, logger

# redmine_webhook rx format
# https://github.com/suer/redmine_webhook
post_payload_example = {
    "example_1": {
        "summary": "Issue opened",
        "value": {
            "payload": {
                "issue": {
                    "author": {
                        "icon_url": "http://www.gravatar.com/avatar/example",
                        "identity_url": None,
                        "lastname": "user",
                        "firstname": "test",
                        "mail": "test@example.com",
                        "login": "test",
                        "id": 3,
                    },
                    "assignee": {
                        "icon_url": "http://www.gravatar.com/avatar/example",
                        "identity_url": None,
                        "lastname": "user",
                        "firstname": "test",
                        "mail": "kimsapdol@rrrrrrr.co.kr",
                        "login": "test",
                        "id": 3,
                    },
                    "priority": {"name": "normal", "id": 2},
                    "tracker": {"name": "bug", "id": 1},
                    "parent_id": None,
                    "root_id": 191,
                    "closed_on": None,
                    "updated_on": "2014-03-01T15:17:48Z",
                    "created_on": "2014-03-01T15:17:48Z",
                    "description": "I'm having a problem with this.",
                    "subject": "Found a bug",
                    "id": 191,
                    "done_ratio": 0,
                    "start_date": "2014-03-02",
                    "due_date": None,
                    "estimated_hours": None,
                    "is_private": False,
                    "lock_version": 0,
                    "project": {
                        "homepage": "",
                        "created_on": "2013-01-12T11:50:26Z",
                        "description": "",
                        "name": "Test Project",
                        "identifier": "test",
                        "id": 4,
                    },
                    "status": {"name": "new", "id": 1},
                },
                "action": "opened",
                "url": "https://example.com",
            }
        },
    },
    "example_2": {
        "summary": "Issue updated",
        "value": {
            "payload": {
                "action": "updated",
                "issue": {
                    "id": 12,
                    "subject": "ㅁㄷㅇㄼㄷㅇㅁㄷㅇ",
                    "description": "ㅂㄷㅇㅂㅈㄷㅇㅂㅈ",
                    "created_on": "2024-06-11T07:04:09.000Z",
                    "updated_on": "2024-06-11T07:04:37.000Z",
                    "closed_on": None,
                    "root_id": 12,
                    "parent_id": None,
                    "done_ratio": 0,
                    "start_date": "2024-06-11",
                    "due_date": None,
                    "estimated_hours": None,
                    "is_private": False,
                    "lock_version": 4,
                    "custom_field_values": [],
                    "project": {
                        "id": 1,
                        "identifier": "test",
                        "name": "TEST",
                        "description": "",
                        "created_on": "2024-05-29T10:01:35.000Z",
                        "homepage": "",
                    },
                    "status": {"id": 3, "name": "해결"},
                    "tracker": {"id": 1, "name": "결함"},
                    "priority": {"id": 2, "name": "보통"},
                    "author": {
                        "id": 1,
                        "login": "admin",
                        "mail": "kimsapdol@rrrrrrr.co.kr",
                        "firstname": "Sapdol",
                        "lastname": "Kim",
                        "identity_url": None,
                        "icon_url": "http://www.gravatar.com/avatar/example",
                    },
                    "assignee": {
                        "id": 1,
                        "login": "admin",
                        "mail": "kimsapdol@rrrrrrr.co.kr",
                        "firstname": "Sapdol",
                        "lastname": "Kim",
                        "identity_url": None,
                        "icon_url": "http://www.gravatar.com/avatar/example",
                    },
                    "watchers": [
                        {
                            "id": 1,
                            "login": "admin",
                            "mail": "kimsapdol@rrrrrrr.co.kr",
                            "firstname": "Sapdol",
                            "lastname": "Kim",
                            "identity_url": None,
                            "icon_url": "http://www.gravatar.com/avatar/example",
                        }
                    ],
                },
                "journal": {
                    "id": 17,
                    "notes": "",
                    "created_on": "2024-06-11T07:04:37.000Z",
                    "private_notes": False,
                    "author": {
                        "id": 1,
                        "login": "admin",
                        "mail": "kimsapdol@rrrrrrr.co.kr",
                        "firstname": "Sapdol",
                        "lastname": "Kim",
                        "identity_url": None,
                        "icon_url": "http://www.gravatar.com/avatar/example",
                    },
                    "details": [
                        {
                            "id": 16,
                            "value": "1",
                            "old_value": None,
                            "prop_key": "assigned_to_id",
                            "property": "attr",
                        }
                    ],
                },
                "url": "http://127.0.0.1/redmine/issues/12",
            }
        },
    },
}


class Message(BaseModel):
    payload: dict[Any, Any]


app = FastAPI(
    redoc_url=None,
    title="Hyobot API Documentation",
    description="""## Hyobot API""",
    summary="Hyobot's KakaoWork Notification API Service",
    version="0.1",
    contact={
        "name": "Kim Sap Dol",
    },
    swagger_ui_parameters={
        "layout": "BaseLayout",
        "deepLinking": True,
        "showExtensions": True,
        "showCommonExtensions": True,
        "tryItOutEnabled": True,
        "requestSnippetsEnabled": True,
    },
)

kakao = Endpoints()


# receives json message and send to kakaowork API
@app.post("/new_message")
def new_message(
    rx_data: Message = Body(
        required=True,
        openapi_examples=post_payload_example,
    ),
) -> JSONResponse:
    data = dict(rx_data)
    print(data)

    action, message = make_message(data)
    # send to kakaowork API

    if action in ["opened", "updated"]:
        logger.info(f"{message=}")
        response = kakao.send_message(**message)
        logger.info(response)
        return JSONResponse(
            content={"action": action, "message": message, "response": response}
        )
    else:
        logger.info(f"Skip sending notification: reason {action}")
        return JSONResponse(
            content={"action": action, "message": message, "response": None}
        )


def generate_description(term: str, content: str) -> dict:
    return {
        "type": "description",
        "term": term,
        "content": {"type": "text", "text": content},
    }


def make_message(data: dict) -> dict:
    """Make message from data"""

    # "priority": {"id": 2, "name": "보통"},

    # get assignee's mail address for receiver
    payload = data.get("payload")

    _ = {
        "text": "해결: [결함][낮음] 13.김효가 말을 안들어요",
        "blocks": [
            {"type": "header", "text": "업데이트 일감 안내"},
            {
                "type": "description",
                "term": "상태",
                "content": {"type": "text", "text": "신규"},
            },
            {
                "type": "description",
                "term": "우선순위",
                "content": {"type": "text", "text": "낮음"},
            },
            {
                "type": "description",
                "term": "저자",
                "content": {"type": "text", "text": "(QA) 김효"},
            },
            {
                "type": "text",
                "text": "text sample",
                "inlines": [
                    {
                        "type": "styled",
                        "text": "김효가 말을 안들어효효효효효효효효효효효효효효효효효효효효효효효효효효효효효효효효효효효",
                    }
                ],
            },
            {"type": "divider"},
            {
                "type": "button",
                "text": "이슈 13 확인",
                "style": "default",
                "action": {
                    "type": "open_system_browser",
                    "name": "button1",
                    "value": "google.com",
                },
            },
        ],
    }

    blocks = []

    # 헤더
    ## 헤더 색상
    issue_priority_id = getDict(payload, ["issue", "priority", "id"])
    header_color = None
    if issue_priority_id == 4:
        header_color = "red"
    elif issue_priority_id == 3:
        header_color = "red"
    elif issue_priority_id == 2:
        header_color = "blue"

    ## 헤더 메세지
    action = getDict(payload, ["action"])
    header_text = "업데이트 일감 안내"
    if action == "opened":
        header_text = "신규 일감 안내"

    block_header = {
        "type": "header",
        "text": header_text,
    }
    if header_color:
        block_header["style"] = header_color
    blocks.append(block_header)

    # 상태
    # "status": {"id": 3, "name": "해결"},
    issue_status = getDict(payload, ["issue", "status", "name"])
    block_status = generate_description("상태", issue_status)
    blocks.append(block_status)

    # 우선순위
    issue_priority = getDict(payload, ["issue", "priority", "name"])
    block_priority = generate_description("우선순위", issue_priority)
    blocks.append(block_priority)

    # 구분
    # "tracker": {"id": 1, "name": "결함"},
    issue_type = getDict(payload, ["issue", "tracker", "name"])
    block_issue_type = generate_description("구분", issue_type)
    blocks.append(block_issue_type)

    # 저자
    author_lastname = getDict(payload, ["issue", "author", "lastname"])
    author_firstname = getDict(payload, ["issue", "author", "firstname"])
    author_name = f"{author_lastname} {author_firstname}"
    block_author = generate_description("저자", author_name)
    blocks.append(block_author)

    # 제목
    issue_subject = getDict(payload, ["issue", "subject"])
    block_subject = {
        "type": "text",
        "text": "text sample",
        "inlines": [
            {
                "type": "styled",
                "text": issue_subject,
            }
        ],
    }
    blocks.append(block_subject)

    # divider
    block_divider = {"type": "divider"}
    blocks.append(block_divider)

    # 버튼
    issue_id = getDict(payload, ["issue", "id"])
    issue_url = getDict(payload, ["url"])
    block_button = {
        "type": "button",
        "text": f"이슈 {issue_id} 확인",
        "style": "default",
        "action": {
            "type": "open_system_browser",
            "name": "button1",
            "value": issue_url,
        },
    }
    blocks.append(block_button)

    # notification text
    fallback_text = (
        f"{issue_status}: [{issue_type}][{issue_priority}] {issue_id}.{issue_subject}"
    )

    recipient_email = getDict(payload, ["issue", "assignee", "mail"])

    return action, {"email": recipient_email, "text": fallback_text, "blocks": blocks}
