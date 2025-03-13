from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import redis

# PostgreSQL Configuration
DATABASE_URL = "postgresql://user:password@localhost/triggerz_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Redis Configuration (for active triggers)
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)