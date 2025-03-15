from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.date import DateTrigger
from database import get_db, SessionLocal
from sqlalchemy.orm import Session
from models import Trigger, ExecutionLog
import datetime

app = FastAPI()
scheduler = BackgroundScheduler()
scheduler.start()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all domains for testing (change in production)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Define a request model
class TriggerRequest(BaseModel):
    trigger_name: str
    trigger_type: str  # "scheduled" or "api"
    delay_seconds: int | None = None
    interval_seconds: int | None = None
    payload: dict | None = None  # Store API trigger data

# Function to execute when the trigger fires
def execute_trigger(trigger_name: str):
    print(f"Trigger '{trigger_name}' executed at {datetime.datetime.now()}")

     # Store execution log in the database
    db = SessionLocal()
    log_entry = ExecutionLog(trigger_name=trigger_name)
    db.add(log_entry)
    db.commit()
    db.close()

@app.get("/")
def read_root():
    return {"message": "Event Trigger System is running!"}

@app.post("/schedule_trigger")
def schedule_trigger(request: TriggerRequest, db: Session = Depends(get_db)):
    """Schedules a trigger (scheduled or API)."""

    # Check if trigger already exists
    existing_trigger = db.query(Trigger).filter(Trigger.name == request.trigger_name).first()
    if existing_trigger:
        return {"error": f"Trigger '{request.trigger_name}' already exists."}

    # Store API triggers correctly with payload
    if request.trigger_type == "api":
        trigger = Trigger(
            name=request.trigger_name,
            trigger_type="api",
            schedule="manual",
            payload=request.payload  # Store API trigger payload
        )
        db.add(trigger)
        db.commit()
        return {"message": f"API trigger '{request.trigger_name}' created. It can be triggered manually."}

    # Store scheduled triggers
    if request.trigger_type == "scheduled":
        schedule_info = None
        if request.delay_seconds:
            run_time = datetime.datetime.now() + datetime.timedelta(seconds=request.delay_seconds)
            scheduler.add_job(
                execute_trigger, 
                DateTrigger(run_date=run_time), 
                args=[request.trigger_name], 
                id=request.trigger_name, 
                replace_existing=True
            )
            schedule_info = f"{request.delay_seconds}s"
        elif request.interval_seconds:
            scheduler.add_job(
                execute_trigger, 
                IntervalTrigger(seconds=request.interval_seconds), 
                args=[request.trigger_name], 
                id=request.trigger_name, 
                replace_existing=True
            )
            schedule_info = f"every {request.interval_seconds}s"
        else:
            return {"error": "Provide 'delay_seconds' or 'interval_seconds' for scheduled triggers."}

        trigger = Trigger(
            name=request.trigger_name,
            trigger_type="scheduled",
            schedule=schedule_info
        )
        db.add(trigger)
        db.commit()
        return {"message": f"Scheduled trigger '{request.trigger_name}' set to run {schedule_info}."}

    return {"error": "Invalid trigger type. Use 'scheduled' or 'api'."}


@app.post("/trigger_api")
def trigger_api(trigger_name: str, db: Session = Depends(get_db)):
    """Manually execute an API trigger."""
    
    # Fetch the API trigger from the database
    trigger = db.query(Trigger).filter(Trigger.name == trigger_name, Trigger.trigger_type == "api").first()
    
    if not trigger:
        return {"error": f"API trigger '{trigger_name}' not found."}

    # Log the execution
    log_entry = ExecutionLog(trigger_name=trigger_name)
    db.add(log_entry)
    db.commit()

    # Ensure payload is returned as JSON
    return {
        "message": f"API trigger '{trigger_name}' executed.",
        "payload": trigger.payload if trigger.payload else "No payload stored"
    }

@app.get("/list_triggers")
def list_triggers(db: Session = Depends(get_db)):
    """List all active triggers from the database and scheduler."""
    
    db_triggers = db.query(Trigger).all()
    active_jobs = scheduler.get_jobs()
    active_triggers = [job.id for job in active_jobs]

    return {
        "db_triggers": [{"name": t.name, "type": t.trigger_type, "schedule": t.schedule} for t in db_triggers],
        "active_triggers": active_triggers
    }

@app.get("/list_logs")
def list_logs(db: Session = Depends(get_db)):
    """Fetch all execution logs."""
    logs = db.query(ExecutionLog).all()
    return [{"trigger_name": log.trigger_name, "executed_at": log.executed_at} for log in logs]

# Define Pydantic Model for JSON Body
class RemoveTriggerRequest(BaseModel):
    trigger_name: str

@app.post("/remove_trigger")
def remove_trigger(request: RemoveTriggerRequest, db: Session = Depends(get_db)):
    """Removes a scheduled trigger from both the database and scheduler."""
    
    job = scheduler.get_job(request.trigger_name)
    if job:
        scheduler.remove_job(request.trigger_name)

    db_trigger = db.query(Trigger).filter(Trigger.name == request.trigger_name).first()
    if db_trigger:
        db.delete(db_trigger)
        db.commit()
        return {"message": f"Trigger '{request.trigger_name}' removed from database and scheduler."}
    
    return {"error": f"Trigger '{request.trigger_name}' not found."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
