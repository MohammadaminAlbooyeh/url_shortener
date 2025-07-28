# backend/database.py
from sqlalchemy import create_engine, Column, Integer, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

DATABASE_URL = "sqlite:///./calorie_tracker.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class CalorieEntry(Base):
    __tablename__ = "calorie_entries"

    id = Column(Integer, primary_key=True, index=True)
    item = Column(String, index=True)
    calories = Column(Integer)
    unit = Column(String)
    date = Column(Date, default=datetime.date.today) # New: Date field

# Create the database tables
Base.metadata.create_all(bind=engine)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()