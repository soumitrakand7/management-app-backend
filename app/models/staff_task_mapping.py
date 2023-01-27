from sqlalchemy import Column, String, ForeignKey, DateTime, Float
from ..db.base_class import default_pk
from sqlalchemy.orm import relationship

from ..db.base_class import Base


class StaffTaskMapping(Base):
    id = Column(String(36), primary_key=True, default=default_pk)
    task_id = Column(String(36), ForeignKey("stafftask.id"))
    staff_id = Column(String(36), ForeignKey("staffmember.id"))

    staff = relationship("StaffMember", foreign_keys=[staff_id])
    task = relationship("StaffTask", foreign_keys=[task_id])
