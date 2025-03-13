from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, redis_client
from models import Trigger
from scheduler import scheduler, execute_trigger
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register_trigger")
def register_trigger(name: str, trigger_type: str, schedule: str = None, event_condition: str = None, db: Session = Depends(get_db)):
    if db.query(Trigger).filter(Trigger.name == name).first():
        raise HTTPException(status_code=400, detail="Trigger already exists")

    trigger = Trigger(name=name, trigger_type=trigger_type, schedule=schedule, event_condition=event_condition)
    db.add(trigger)
    db.commit()

    if trigger_type == "periodic":
        scheduler.add_job(execute_trigger, IntervalTrigger(seconds=int(schedule)), args=[name], id=name)
    elif trigger_type == "event-driven":
        redis_client.set(name, "waiting")

    return {"message": "Trigger registered", "trigger": name}

@router.get("/execute_trigger/{name}")
def execute_event_trigger(name: str):
    if redis_client.get(name) == "waiting":
        execute_trigger(name)
        return {"message": f"Event trigger '{name}' executed"}
    raise HTTPException(status_code=404, detail="Trigger not found")

@router.get("/list_triggers")
def list_triggers(db: Session = Depends(get_db)):
    triggers = db.query(Trigger).all()
    return {"triggers": [trigger.name for trigger in triggers]}