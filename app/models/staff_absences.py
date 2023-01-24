from sqlalchemy import Boolean, Column, Date, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from ..db.base_class import Base, default_pk


class StaffAbsence(Base):
    id = Column(String(36), primary_key=True, default=default_pk)
    staff_id = Column(String(36), ForeignKey("staffmember.id"))
    abscence_date = Column(Date, nullable=False)

    staff_member = relationship("StaffMember", foreign_keys=[staff_id])
