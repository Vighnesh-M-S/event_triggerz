from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
import redis

scheduler = BackgroundScheduler()
scheduler.start()

redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

def execute_trigger(trigger_name):
    """Simulate trigger execution."""
    print(f"Executing trigger: {trigger_name}")
    redis_client.set(trigger_name, "executed")