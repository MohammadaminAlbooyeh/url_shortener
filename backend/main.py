# backend/main.py
from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import List, Optional
import datetime
import sqlite3
import pandas as pd # For CSV export

app = FastAPI()

# --- Database Setup using sqlite3 ---
DATABASE_FILE = "calorie_tracker_sqlite3.db"

def get_db_connection():
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row # This allows accessing columns by name
    return conn

def create_table_if_not_exists():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS calorie_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item TEXT NOT NULL,
            calories INTEGER NOT NULL,
            unit TEXT NOT NULL,
            entry_date TEXT NOT NULL -- Storing date as TEXT in YYYY-MM-DD format
        )
    """)
    conn.commit()
    conn.close()

# Ensure table is created when the app starts
create_table_if_not_exists()

# Pydantic models
class CalorieEntryBase(BaseModel):
    item: str
    calories: int
    unit: str

class CalorieEntryCreate(CalorieEntryBase):
    pass

class CalorieEntryResponse(CalorieEntryBase):
    id: int
    date: datetime.date # Still expose as date object in API response

class MaxDailyCalories(BaseModel):
    max_daily_calories: int = 2000 # Default max daily calories

# Global variable for max daily calories
MAX_DAILY_CALORIES = 2000

# Helper function to convert sqlite3.Row to CalorieEntryResponse
def row_to_calorie_entry(row):
    return CalorieEntryResponse(
        id=row['id'],
        item=row['item'],
        calories=row['calories'],
        unit=row['unit'],
        date=datetime.date.fromisoformat(row['entry_date'])
    )

# --- API Endpoints ---

@app.post("/add_calorie_entry/", response_model=CalorieEntryResponse)
def add_calorie_entry(entry: CalorieEntryCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    current_date_str = datetime.date.today().isoformat() # YYYY-MM-DD
    try:
        cursor.execute(
            "INSERT INTO calorie_entries (item, calories, unit, entry_date) VALUES (?, ?, ?, ?)",
            (entry.item, entry.calories, entry.unit, current_date_str)
        )
        conn.commit()
        # Get the last inserted row to return it
        cursor.execute("SELECT * FROM calorie_entries WHERE id = last_insert_rowid()")
        new_entry = cursor.fetchone()
        return row_to_calorie_entry(new_entry)
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error: {e}")
    finally:
        conn.close()

@app.get("/get_entries/", response_model=List[CalorieEntryResponse])
def get_entries(date: Optional[datetime.date] = None):
    conn = get_db_connection()
    cursor = conn.cursor()
    query_date_str = date.isoformat() if date else datetime.date.today().isoformat()

    try:
        cursor.execute(
            "SELECT * FROM calorie_entries WHERE entry_date = ?",
            (query_date_str,)
        )
        rows = cursor.fetchall()
        return [row_to_calorie_entry(row) for row in rows]
    finally:
        conn.close()

@app.get("/get_total_calories/")
def get_total_calories(date: Optional[datetime.date] = None):
    conn = get_db_connection()
    cursor = conn.cursor()
    query_date_str = date.isoformat() if date else datetime.date.today().isoformat()

    try:
        cursor.execute(
            "SELECT SUM(calories) FROM calorie_entries WHERE entry_date = ?",
            (query_date_str,)
        )
        total_calories = cursor.fetchone()[0] or 0 # .fetchone() returns a tuple, get first element
        return {"total_calories": total_calories, "max_daily_calories": MAX_DAILY_CALORIES}
    finally:
        conn.close()

@app.post("/reset_calories/")
def reset_calories(date: Optional[datetime.date] = None):
    conn = get_db_connection()
    cursor = conn.cursor()
    query_date_str = date.isoformat() if date else datetime.date.today().isoformat()

    try:
        cursor.execute(
            "DELETE FROM calorie_entries WHERE entry_date = ?",
            (query_date_str,)
        )
        conn.commit()
        return {"message": f"Calories for {query_date_str} reset successfully!"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error: {e}")
    finally:
        conn.close()

@app.get("/get_all_entries/", response_model=List[CalorieEntryResponse])
def get_all_entries():
    """Fetches all historical calorie entries."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM calorie_entries ORDER BY entry_date ASC, id ASC")
        rows = cursor.fetchall()
        return [row_to_calorie_entry(row) for row in rows]
    finally:
        conn.close()