from typing import Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ... import crud, models
from .. import deps
from starlette.websockets import WebSocket, WebSocketDisconnect, WebSocketState
from integrations import socket

router = APIRouter()


@router.websocket("/create-chat/")
async def websocket_endpoint(
    chat_dict: Dict,
    db: Session = Depends(deps.get_db),
    websocket: WebSocket = WebSocket,
    current_user: models.Users = Depends(deps.get_current_user),
):
    room_name = chat_dict.get('room_name')
    try:
        await socket.connect(websocket, room_name)
        crud.chats.create_room(
            db=db,
            first_user_email=current_user,
            second_user_email=chat_dict.get('second_user_email')
        )
        all_chats = crud.chats.get_chats(db=db, chat_id=room_name)
        await socket.broadcast(all_chats)

        while True:
            try:
                if websocket.application_state == WebSocketState.CONNECTED:
                    data = await websocket.receive_text()
                    crud.chats.create_chat(
                        db=db, chat_id=room_name, message=data)
                    all_chats = crud.chats.get_chats(db=db, chat_id=room_name)
                else:
                    await socket.connect(websocket, room_name)
            except WebSocketDisconnect:
                print("[ERR] chat/room/ websocket.application_state error occured.")
                socket.disconnect(websocket, room_name)
                break

    except WebSocketDisconnect:
        socket.disconnect(websocket, room_name)


@router.websocket("/get-chats/")
async def listen_messages(
    db: Session = Depends(deps.get_db),
    websocket: WebSocket = WebSocket,
    room_name: str = None,
    current_user: models.Users = Depends(deps.get_current_user),
):
    try:
        await socket.connect(websocket, room=room_name)
        initial_data = crud.chats.get_chats(db=db, chat_id=room_name)

        await socket.broadcast(initial_data)
        while True:
            try:
                if websocket.application_state == WebSocketState.CONNECTED:
                    data = await websocket.receive_text()
                    socket.broadcast(data=data)
                else:
                    socket.connect(websocket=websocket, room=room_name)

            except WebSocketDisconnect as e:
                print("ERR WebSocketDisconnect   ", current_user)
                print(e)
                socket.disconnect(websocket=websocket, room=room_name)
                break

    except WebSocketDisconnect:
        socket.disconnect(websocket=websocket, room=room_name)
        print(e, "\n\n\n")
