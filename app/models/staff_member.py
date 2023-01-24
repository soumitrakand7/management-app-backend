from sqlalchemy import Boolean, Column, String, Text, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from ..db.base_class import default_pk

from ..db.base_class import Base


class StaffMember(Base):
    id = Column(String(36), primary_key=True, default=default_pk)
    user_email = Column(String(36), ForeignKey("users.email"))
    designation = Column(String(24), index=True, nullable=False)
    job_details = Column(Text)
    employment_status = Column(String(24))  # employed / unemployed

    user = relationship("Users", foreign_keys=[user_email])
