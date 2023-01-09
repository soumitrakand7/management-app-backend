from sqlalchemy import Boolean, Column, String, Text, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from ..db.base_class import default_pk

from ..db.base_class import Base


class GuestMember(Base):
    id = Column(String(36), primary_key=True, default=default_pk)
    user_email = Column(String(32), ForeignKey("users.email"))
    relation_tag = Column(String(32), index=True, nullable=False)

    user = relationship("Users", foreign_keys=[user_email])
