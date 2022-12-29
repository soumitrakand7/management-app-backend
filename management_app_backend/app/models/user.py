from sqlalchemy import Boolean, Column, String, Text

from ..db.base_class import Base


class Users(Base):
    email = Column(String(32), unique=True, index=True,
                   primary_key=True, nullable=False)
    first_name = Column(String(32), index=True)
    last_name = Column(String(32))
    mobile_no = Column(String(10), index=True, nullable=False)
    address = Column(Text)
    hashed_password = Column(String(512))
    is_active = Column(Boolean(), default=False)
