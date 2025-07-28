# backend/check_db.py (or any other location)
import sqlite3
import datetime

DATABASE_FILE = "calorie_tracker_sqlite3.db"

def get_all_entries():
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM calorie_entries ORDER BY entry_date ASC, id ASC")
    rows = cursor.fetchall()
    conn.close()

    for row in rows:
        # You can access columns by name because of row_factory = sqlite3.Row
        entry_date = datetime.date.fromisoformat(row['entry_date'])
        print(f"ID: {row['id']}, Date: {entry_date}, Item: {row['item']}, Calories: {row['calories']}, Unit: {row['unit']}")

if __name__ == "__main__":
    # Make sure to run this script from the 'backend' directory
    # or adjust DATABASE_FILE path accordingly
    print("--- All Calorie Entries ---")
    get_all_entries()