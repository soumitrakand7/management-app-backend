from sqlalchemy import Boolean, Column, String, Text, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from ..db.base_class import default_pk

from ..db.base_class import Base


class FamilyMember(Base):
    id = Column(String(36), primary_key=True, default=default_pk)
    relation_tag = Column(String(24), nullable=False, index=True)
    user_email = Column(String(32), ForeignKey("users.email"))

    user = relationship("Users", foreign_keys=[user_email])
