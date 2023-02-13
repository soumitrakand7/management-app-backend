from sqlalchemy import Boolean, Column, String, Text, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from ..db.base_class import default_pk

from ..db.base_class import Base


class ChatRoom(Base):
    id = Column(String(36), primary_key=True, default=default_pk)
    first_user_email = Column(String(36), ForeignKey("users.email"))
    secoond_user_email = Column(String(36), ForeignKey("users.email"))
    chat_id = Column(String(64), nullable=False, unique=True)
    last_message = Column(Text)

    first_user = relationship("Users", foreign_keys=[first_user_email])
    secoond_user = relationship("Users", foreign_keys=[secoond_user_email])
