from fastapi import FastAPI, Depends
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.date import DateTrigger
from database import get_db
from sqlalchemy.orm import Session
from models import Trigger
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
    delay_seconds: int | None = None
    interval_seconds: int | None = None

# Function to execute when the trigger fires
def execute_trigger(trigger_name: str):
    print(f"Trigger '{trigger_name}' executed at {datetime.datetime.now()}")

@app.post("/schedule_trigger")
def schedule_trigger(request: TriggerRequest):
    """Schedules a trigger to execute after a delay (one-time) or at an interval (recurring)."""
    if request.delay_seconds:
        run_time = datetime.datetime.now() + datetime.timedelta(seconds=request.delay_seconds)
        scheduler.add_job(execute_trigger, DateTrigger(run_date=run_time), args=[request.trigger_name], id=request.trigger_name, replace_existing=True)
        return {"message": f"One-time trigger '{request.trigger_name}' scheduled in {request.delay_seconds} seconds."}
    
    if request.interval_seconds:
        scheduler.add_job(execute_trigger, IntervalTrigger(seconds=request.interval_seconds), args=[request.trigger_name], id=request.trigger_name, replace_existing=True)
        return {"message": f"Recurring trigger '{request.trigger_name}' set to run every {request.interval_seconds} seconds."}
    
    return {"error": "Provide either 'delay_seconds' (for one-time trigger) or 'interval_seconds' (for recurring trigger)."}

@app.get("/list_triggers")
def list_triggers():
    """Lists all active scheduled triggers."""
    jobs = scheduler.get_jobs()
    return {"scheduled_triggers": [job.id for job in jobs]}

# Define Pydantic Model for JSON Body
class RemoveTriggerRequest(BaseModel):
    trigger_name: str

@app.post("/remove_trigger")
def remove_trigger(request: RemoveTriggerRequest, db: Session = Depends(get_db)):
    """Removes a scheduled trigger."""
    job = scheduler.get_job(request.trigger_name)
    if job:
        scheduler.remove_job(request.trigger_name)

    db_trigger = db.query(Trigger).filter(Trigger.name == request.trigger_name).first()
    if db_trigger:
        db.delete(db_trigger)
        db.commit()

    return {"message": f"Trigger '{request.trigger_name}' removed."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
