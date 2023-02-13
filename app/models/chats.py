from sqlalchemy import Boolean, Column, String, Text, DateTime
from ..db.base_class import default_pk

from ..db.base_class import Base


class Chats(Base):
    id = Column(String(36), primary_key=True, default=default_pk)
    chat_id = Column(String(64))
    message = Column(Text)
    sender = Column(String(36))
    time_stamp = Column(DateTime)
