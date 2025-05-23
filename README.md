# Event Trigger Mechanism �

A FastAPI-based event trigger system where users can schedule or manually trigger events via API. Supports:
- ✅ **Scheduled Triggers** – One-time or recurring execution
- ✅ **API Triggers** – Manually triggered with custom payloads
- ✅ **Execution Logs** – Stores trigger execution details
- ✅ **Frontend UI** – Manage triggers from a web interface
- ✅ **Docker & Cloud Deployment** – Runs via Docker locally & deployed on Render

## 📌 Features
- **Scheduled Trigger**: Runs at a fixed time or interval.
- **API Trigger**: Triggers on-demand via API.
- **Logging System**: Stores execution logs with retention & expiry rules.
- **User-Friendly Web UI**: Manage and view triggers.
- **Dockerized & Cloud-Ready**: Works with Docker, deployed on Render.

## 🌐 Live Deployment
The application is deployed on Render. You can access it here:  

🔗 **[Event Trigger System](https://event-triggerz.onrender.com/)**  

## 🛠️ Local Setup (Without Docker)

### 1️⃣ Install Dependencies

Ensure you have Python 3.10+ installed. Then, run:

```bash
# Clone the repository
git clone https://github.com/yourusername/event-trigger-system.git
cd event-trigger-system

# Create virtual environment
python -m venv venv
source venv/bin/activate   # For macOS/Linux
venv\Scripts\activate      # For Windows

# Install dependencies
pip install -r requirements.txt

```

### 2️⃣ Set Up the Database
Using SQLite (default):
```bash
sqlite3 event_triggers.db < setup.sql
```
### 🔹 1. Automatic Database Migration Using Python

```bash
python
```

```python
from models import Base
target_metadata = Base.metadata
exit()
```


### 🔹 2. Manual Database Setup Using SQLite

#### 📌 2.1. Open SQLite CLI

```bash
sqlite3 event_triggers.db
```

#### 📌 2.2. Create Tables Manually

If you prefer to create tables manually, execute the following:
##### ✅ Create triggers Table

```sql
CREATE TABLE triggers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    trigger_type TEXT NOT NULL CHECK(trigger_type IN ('scheduled', 'api')),
    schedule TEXT,
    payload TEXT
);
```
##### ✅ Create execution_logs Table

```sql
CREATE TABLE execution_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    trigger_name TEXT NOT NULL,
    executed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(trigger_name) REFERENCES triggers(name) ON DELETE CASCADE
);
```

#### 📌 2.3. Verify Table Creation

```sql
PRAGMA table_info(triggers);
PRAGMA table_info(execution_logs);
```

### 3️⃣ Run the Application
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

- Visit **http://127.0.0.1:8000** to access the application.

## 🐳 Running with Docker

### 1️⃣ Install Docker

Ensure you have Docker installed:

```bash
docker --version
```

### 2️⃣ Build and Run Docker Container

```bash
docker build -t event-trigger-app .
docker run -p 8000:8000 event-trigger-app
```

- The application will be available at **http://localhost:8000**.


### 3️⃣ Stopping the Container

To stop the running container:

```bash
docker ps            # Find container ID
docker stop <ID>     # Stop container
docker rm <ID>       # Remove container
```



## 🔗 API Endpoints

### 📌 Trigger Management

| Method | Endpoint            | Description                     |
|--------|---------------------|---------------------------------|
| POST   | `/schedule_trigger`  | Schedule a new event trigger    |
| GET    | `/list_triggers`     | Retrieve all scheduled triggers |
| POST   | `/remove_trigger`    | Remove a scheduled trigger      |
| PUT    | `/update_trigger`    | Update an existing trigger      |
### 🔥 Execution & Testing

| Method | Endpoint            | Description                              |
|--------|---------------------|------------------------------------------|
| POST   | `/trigger_api`      | Manually trigger an API event            |
| GET    | `/list_logs`        | View execution logs                      |
| POST   | `/test_trigger`     | Test a trigger without saving it         |



### 🟢 Create a Trigger

```http
POST /schedule_trigger
Content-Type: application/json

{
  "trigger_name": "test_trigger",
  "trigger_type": "scheduled",
  "delay_seconds": 10
}

```

### 🟢 List All Triggers

```http
GET /list_triggers
```

### 🟢 Manually Trigger API Trigger

```http
POST /trigger_api?trigger_name=api_test
```


### 🟢 Remove a Trigger

```http
POST /remove_trigger
Content-Type: application/json

{
  "trigger_name": "test_trigger"
}
```

### 🟢 Test a Trigger (One-time Execution Without Saving)

```http
POST /test_trigger  
Content-Type: application/json  

{
  "trigger_name": "test_trigger",
  "trigger_type": "scheduled",
  "delay_seconds": 10
}
```

### 🟢 For an API trigger test

```http
POST /test_trigger  
Content-Type: application/json  

{
  "trigger_name": "api_test_trigger",
  "trigger_type": "api",
  "payload": { "message": "This is a test API trigger" }
}
```

### 🟢 For updating trigger(scheduled)

```http
PUT /update_trigger
Content-Type: application/json

{
  "trigger_name": "test_trigger",
  "trigger_type": "scheduled",
  "delay_seconds": 20
}
```

### 🟢 For updating trigger(api)

```http
PUT /update_trigger
Content-Type: application/json

{
  "trigger_name": "api_test_trigger",
  "trigger_type": "api",
  "payload": "Hello from API Trigger"
}
```

### 🟢 Fetch Trigger Execution Logs

```http
GET /list_logs 
```

### 🎨 Frontend Access

The frontend is accessible via `index.html` at:  
🔗 [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## 📚 Credits & Resources

During the development of this project, the following resources were used:

- **ChatGPT** - Assistance with debugging, SQL queries, and FastAPI implementation.
- **FastAPI Documentation** - Official documentation for building and deploying APIs. [FastAPI Docs](https://fastapi.tiangolo.com/)
- **Render** - Cloud deployment service for hosting the application. [Render](https://render.com/)
- **Docker Documentation** - Used for containerizing the application. [Docker Docs](https://docs.docker.com/)
- **SQLAlchemy Documentation** - ORM used for managing the database. [SQLAlchemy Docs](https://www.sqlalchemy.org/)
- **SQLite** - The database used for local development. [SQLite Docs](https://www.sqlite.org/)
- **Stack Overflow** - Solutions to various programming issues encountered.

