from sqlalchemy import Boolean, Column, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from ..db.base_class import default_pk

from ..db.base_class import Base


class StaffTree(Base):
    id = Column(String(36), primary_key=True, default=default_pk)
    staff_id = Column(String(36), ForeignKey("staffmember.id"))
    senior_staff_id = Column(String(36), ForeignKey("staffmember.id"))
    relation_tag = Column(String(24), nullable=False)
    subscriber_group_id = Column(String(36), nullable=False)

    staff_member = relationship("StaffMember", foreign_keys=[staff_id])
    senior_staff_member = relationship(
        "StaffMember", foreign_keys=[senior_staff_id])


__table_args__ = (
    UniqueConstraint('staff_id', 'senior_staff_id')
)
