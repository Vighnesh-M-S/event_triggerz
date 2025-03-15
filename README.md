# Event Trigger System �

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

## 📚 API Endpoints

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