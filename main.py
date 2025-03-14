from fastapi import FastAPI
# import uvicorn
# from routes import router
# from scheduler import scheduler

# app = FastAPI(title="Event Trigger System")

# app.include_router(router)

# @app.on_event("shutdown")
# def shutdown_scheduler():
#     scheduler.shutdown()

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to Event trigger system "}

@app.post("/trigger_event")
def trigger_event():
    return {"status": "success", "message": "Event triggered successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)