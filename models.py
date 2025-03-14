from sqlalchemy import Column, Integer, String, DateTime
from database import Base
import datetime

class Trigger(Base):
    __tablename__ = "triggers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    trigger_type = Column(String)  # "scheduled" or "api"
    schedule = Column(String, nullable=True)  # Stores interval like "10s"
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
