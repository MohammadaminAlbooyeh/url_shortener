# main.py for FastAPI Backend
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI(
    title="Calorie Tracker API",
    description="A simple API to track daily calorie intake."
)

# In-memory storage for calorie entries.
# In a real application, this would be replaced with a database (e.g., PostgreSQL, MongoDB).
calorie_entries: List[Dict[str, int]] = []
# We'll keep a simple running total for the "day" as per the request,
# without complex date handling for simplicity.
# For a real app, you'd associate entries with specific dates and users.
current_total_calories: int = 0

class CalorieEntry(BaseModel):
    """
    Pydantic model for a single calorie entry.
    """
    item: str
    calories: int

class CalorieSummary(BaseModel):
    """
    Pydantic model for the total calorie summary.
    """
    total_calories: int
    max_daily_calories: int = 2000

@app.post("/add_calorie_entry/", response_model=CalorieSummary)
async def add_calorie_entry(entry: CalorieEntry):
    """
    Adds a new calorie entry to the tracker and updates the total.
    """
    global current_total_calories
    calorie_entries.append({"item": entry.item, "calories": entry.calories})
    current_total_calories += entry.calories
    return CalorieSummary(total_calories=current_total_calories)

@app.get("/get_total_calories/", response_model=CalorieSummary)
async def get_total_calories():
    """
    Retrieves the current total calorie intake.
    """
    return CalorieSummary(total_calories=current_total_calories)

@app.post("/reset_calories/", response_model=CalorieSummary)
async def reset_calories():
    """
    Resets the calorie tracker for a new day.
    """
    global calorie_entries
    global current_total_calories
    calorie_entries = []
    current_total_calories = 0
    return CalorieSummary(total_calories=current_total_calories)

# To run this FastAPI application:
# 1. Save the code above as `main.py`.
# 2. Install FastAPI and Uvicorn: `pip install fastapi uvicorn`
# 3. Run the server: `uvicorn main:app --reload`
# The API will be available at http://127.0.0.1:8000
