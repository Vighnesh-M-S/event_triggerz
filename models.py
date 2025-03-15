from sqlalchemy import Column, Integer, String, DateTime
from database import Base
from datetime import datetime, timezone

class Trigger(Base):
    __tablename__ = "triggers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    trigger_type = Column(String)  # "scheduled" or "event-driven"
    schedule = Column(String, nullable=True)  # Stores interval like "10s"
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
