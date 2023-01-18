from sqlalchemy import Boolean, Column, String, Text, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from ..db.base_class import default_pk
from sqlalchemy import Column, String, UniqueConstraint

from ..db.base_class import Base


class FamilyMember(Base):
    id = Column(String(36), primary_key=True, default=default_pk)
    child_email = Column(String(36), ForeignKey("users.email"), nullable=False)
    parent_email = Column(String(36), ForeignKey("users.email"))
    subscriber_group_id = Column(String(36), nullable=False)

    child = relationship("Users", foreign_keys=[child_email])
    parent = relationship("Users", foreign_keys=[parent_email])


__table_args__ = (
    UniqueConstraint('child_email', 'parent_email')
)
