"""FastAPI Server which receives as POST and sends to kakaowork API
"""

from typing import Any
import json

from fastapi import FastAPI, Body, Request, Response, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
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
                        "mail": "kimjeonghyo@rhaon.co.kr",
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
                "url": "https://example.com",
                "journal": {
                    "details": [],
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
                        "mail": "kimjeonghyo@rhaon.co.kr",
                        "login": "test",
                        "id": 3,
                    },
                    "private_notes": False,
                    "created_on": "2014-03-01T16:22:46Z",
                    "notes": "Fixed",
                    "id": 195,
                },
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
                    "priority": {"name": "normal", "id": 2},
                    "tracker": {"name": "bug", "id": 1},
                    "parent_id": None,
                    "root_id": 196,
                    "closed_on": None,
                    "updated_on": "2014-03-01T16:22:46Z",
                    "created_on": "2014-03-01T15:44:22Z",
                    "description": "test",
                    "subject": "Found a bug",
                    "id": 196,
                    "done_ratio": 0,
                    "start_date": "2014-03-02",
                    "due_date": None,
                    "estimated_hours": None,
                    "is_private": False,
                    "lock_version": 2,
                    "project": {
                        "homepage": "",
                        "created_on": "2013-01-12T11:50:26Z",
                        "description": "",
                        "name": "Test Project",
                        "identifier": "test",
                        "id": 4,
                    },
                    "status": {"name": "normal", "id": 1},
                },
                "action": "updated",
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
        "name": "Kim Jeong Hyo",
        "email": "kimjeonghyo@rhaon.co.kr",
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
    )
) -> JSONResponse:
    data = dict(rx_data)
    print(data)

    action, message = make_message(data)
    # send to kakaowork API

    if action == "opened":
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


def make_message(data: dict) -> dict:
    """Make message from data"""

    # get assignee's mail address for receiver
    payload = data.get("payload")
    email = getDict(payload, ["issue", "assignee", "mail"])
    tracker_subject = getDict(payload, ["issue", "subject"])
    tracker_id = getDict(payload, ["issue", "id"])
    tracker_type = getDict(payload, ["tracker", "name"])
    tracker_priority = getDict(payload, ["priority", "name"])
    action = getDict(payload, ["action"])
    url = getDict(payload, ["url"])

    # format message
    fallback_text = f"[{tracker_type}] {tracker_id}.{tracker_subject}"

    block_message = [
        {
            "type": "text",
            "text": "text sample",
            "inlines": [
                {
                    "type": "styled",
                    "text": f"{tracker_type} ",
                    "bold": True,
                    "color": "red",
                },
                {"type": "styled", "text": f"[{tracker_priority}] "},
                {"type": "styled", "text": tracker_subject},
            ],
        },
        {
            "type": "button",
            "text": f"이슈 {tracker_id} 바로가기",
            "style": "default",
            "action": {
                "type": "open_system_browser",
                "name": "button1",
                "value": url,
            },
        },
    ]

    return action, {"email": email, "text": fallback_text, "blocks": block_message}
