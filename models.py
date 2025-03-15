from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime, timezone

class Trigger(Base):
    __tablename__ = "triggers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    trigger_type = Column(String)  # "scheduled" or "event-driven"
    schedule = Column(String, nullable=True)  # Stores interval like "10s"
    payload = Column(JSON, nullable=True)  # Store API request data
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    logs = relationship("ExecutionLog", back_populates="trigger")

class ExecutionLog(Base):
    __tablename__ = "execution_logs"

    id = Column(Integer, primary_key=True, index=True)
    trigger_name = Column(String, ForeignKey("triggers.name"))  # Foreign key to link with Trigger
    executed_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))  # Execution time

    trigger = relationship("Trigger", back_populates="logs")  # Relationship to trigger
