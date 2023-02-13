from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import Chats, ChatRoom
from datetime import datetime


class CRUDChat(CRUDBase):
    def create_room(
        self,
        db: Session,
        first_user_email: str,
        second_user_email: str
    ):
        room_id = self.get_room_id(
            first_user_email=first_user_email, second_user_email=second_user_email)
        chat_room_obj = db.query(ChatRoom).filter(
            ChatRoom.chat_id == room_id).first()
        if chat_room_obj is not None:
            return chat_room_obj
        room_obj = ChatRoom(
            first_user_email=first_user_email,
            secoond_user_email=second_user_email,
            chat_id=room_id
        )
        db.add(room_obj)
        db.commit()
        db.refresh(room_obj)

    def get_chat_room(self, db: Session, room_id: str):
        return db.query(ChatRoom).filter(ChatRoom.chat_id == room_id).first()

    def create_chat(
        self,
        db: Session,
        chat_id: str,
        message: str,
        sender: str
    ):
        chat_obj = Chats(
            chat_id=chat_id,
            message=message,
            sender=sender,
            time_stamp=datetime.now()
        )
        db.add(chat_obj)
        db.commit()
        db.refresh(chat_obj)

        chat_room_obj = db.query(ChatRoom).filter(
            ChatRoom.chat_id == chat_id).first()
        setattr(chat_room_obj, 'last_message', message)
        db.add(chat_room_obj)
        db.commit()
        db.refresh(chat_room_obj)

        return chat_obj

    def get_room_id(self, first_user_email: str, second_user_email: str):
        x = ""
        y = ""
        if first_user_email > second_user_email:
            x = second_user_email
            y = first_user_email
        else:
            x = first_user_email
            y = second_user_email
        room_id = x.split(
            "@")[0] + "_" + y.split("@")[0] + "_room"
        return room_id

    def get_chats(self, db: Session, chat_id: str):
        chats = db.query(Chats).filter(Chats.chat_id == chat_id).all()
        return chats

    def get_chats_by_user(self, db: Session, user_email: str):
        substr = user_email.split("@")[0]
        chat_rooms = db.query(ChatRoom).filter(
            substr in ChatRoom.chat_id).all()
        return chat_rooms


chats = CRUDChat()
