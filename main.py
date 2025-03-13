from fastapi import FastAPI
import uvicorn
from routes import router
from scheduler import scheduler

app = FastAPI(title="Event Trigger System")

app.include_router(router)

@app.on_event("shutdown")
def shutdown_scheduler():
    scheduler.shutdown()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)