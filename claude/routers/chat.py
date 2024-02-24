from typing import List, Dict, Union, Any
from jinja2 import Environment, FileSystemLoader
from fastapi.templating import Jinja2Templates
from fastapi import (
    WebSocket, WebSocketDisconnect, APIRouter, Request
)


if __name__ == 'routers.chat':
    from services import anthropic_svc
else:
    from ..services import anthropic_svc


router = APIRouter()
templates = Jinja2Templates(env=Environment(loader=FileSystemLoader('templates')))

class SocketManager:
    def __init__(self):
        self.active_connections: List[(WebSocket, str)] = []

    async def connect(self, websocket: WebSocket, user: str):
        await websocket.accept()
        self.active_connections.append((websocket, user))

    def disconnect(self, websocket: WebSocket, user: str):
        self.active_connections.remove((websocket, user))

    async def send_personal_message(self,
                                    data: Dict[str, Union[str, Any]],
                                    websocket: WebSocket):
        """Direct Message"""
        await websocket.send_json(data)

    async def broadcast(self, data):
        for connection in self.active_connections:
            await connection[0].send_json(data)


socket_manager = SocketManager()


@router.websocket("/api/chat")
async def websocket_endpoint(websocket: WebSocket):
    sender = websocket.cookies.get("X-Authorization")
    await socket_manager.connect(websocket, sender)
    response = {
        "sender": sender,
        "message": "got connected"
    }
    await socket_manager.broadcast(response)
    try:
        while True:
            data = await websocket.receive_json()
            await socket_manager.send_personal_message(
                data, websocket
            )
            resp = await treat_response(sender, data)
            await socket_manager.send_personal_message(
                data=resp, websocket=websocket
            )
    except WebSocketDisconnect:
        socket_manager.disconnect(websocket, sender)
        response['message'] = "left"
        await socket_manager.broadcast(response)


async def treat_response(sender, prompt):
    print(sender)
    print(prompt)
    resp = await anthropic_svc.do_request(prompt)
    response = {
        "sender": "claude.ai",
        "message": resp
    }
    print(response)
    return response


@router.get("/chat")
def get_chat(request: Request):
    return templates.TemplateResponse("chat.html", {
        "request": request
    })
