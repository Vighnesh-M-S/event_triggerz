from sqlalchemy import Column, String, Integer
from database import Base

class Trigger(Base):
    __tablename__ = "triggers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    trigger_type = Column(String)  # "periodic" or "event-driven"
    schedule = Column(String, nullable=True)  # Only for periodic triggers
    event_condition = Column(String, nullable=True)  # Only for event-driven