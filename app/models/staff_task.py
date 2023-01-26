from sqlalchemy import Boolean, Column, String, Text, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from ..db.base_class import default_pk

from ..db.base_class import Base


class StaffTask(Base):
    id = Column(String(36), primary_key=True, default=default_pk)
    staff_id = Column(String(36), ForeignKey("staffmember.id"))
    task_title = Column(String(36), nullable=False)
    description = Column(Text)
    assigned_at = Column(DateTime)
    valid_for = Column(Float)

    staff_member = relationship("StaffMember", foreign_keys=[staff_id])
