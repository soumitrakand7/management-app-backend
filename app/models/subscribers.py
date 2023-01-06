from sqlalchemy import Boolean, Column, String, Text, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship

from datetime import datetime
from ..db.base_class import Base


class Subscriber(Base):
    user_email = Column(String(32), ForeignKey())
    