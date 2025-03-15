Event Trigger System 🚀

A FastAPI-based event trigger system where users can schedule or manually trigger events via API. Supports:✅ Scheduled Triggers – One-time or recurring execution✅ API Triggers – Manually triggered with custom payloads✅ Execution Logs – Stores trigger execution details✅ Frontend UI – Manage triggers from a web interface✅ Docker & Cloud Deployment – Runs via Docker locally & deployed on Render

📌 Features

Scheduled Trigger: Runs at a fixed time or interval.

API Trigger: Triggers on-demand via API.

Logging System: Stores execution logs with retention & expiry rules.

User-Friendly Web UI: Manage and view triggers.

Dockerized & Cloud-Ready: Works with Docker, deployed on Render.

🛠️ Local Setup (Without Docker)

1️⃣ Install Dependencies

Ensure you have Python 3.10+ installed. Then, run:

# Clone the repository
git clone https://github.com/yourusername/event-trigger-system.git
cd event-trigger-system

# Create virtual environment
python -m venv venv
source venv/bin/activate   # For macOS/Linux
venv\Scripts\activate      # For Windows

# Install dependencies
pip install -r requirements.txt

2️⃣ Set Up the Database

Using SQLite (default):

sqlite3 event_triggers.db < setup.sql

If using PostgreSQL (Optional):

export DATABASE_URL=postgresql://user:password@localhost:5432/event_triggers

3️⃣ Run the Application

uvicorn main:app --host 0.0.0.0 --port 8000 --reload

Visit http://127.0.0.1:8000 to access the API.Visit http://127.0.0.1:8000/static/index.html for the frontend.

🐳 Running with Docker

1️⃣ Install Docker

Ensure you have Docker installed:

docker --version

2️⃣ Build and Run Docker Container

docker build -t event-trigger-app .
docker run -p 8000:8000 event-trigger-app

The API will be available at http://localhost:8000

The Frontend UI will be available at http://localhost:8000/static/index.html

3️⃣ Stopping the Container

To stop the running container:

docker ps            # Find container ID
docker stop <ID>     # Stop container
docker rm <ID>       # Remove container

🌍 Deploying on Render

Create a Render Web Service at Render.com.

Connect GitHub repository & set build command:

docker build -t event-trigger-app .

Expose port 8000.

Ensure Render runs:

docker run -p 8000:8000 event-trigger-app

Live Deployment: 👉 Your Render App Link Here

📚 API Endpoints

🟢 Create a Trigger

POST /schedule_trigger
Content-Type: application/json
{
  "trigger_name": "test_trigger",
  "trigger_type": "scheduled",
  "delay_seconds": 10
}

🟢 List All Triggers

GET /list_triggers

🟢 Manually Trigger API Trigger

POST /trigger_api?trigger_name=api_test

🟢 Remove a Trigger