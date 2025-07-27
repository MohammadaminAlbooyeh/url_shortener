# Calorie Tracker

Track your daily calorie intake with a modern web interface and backend API.

## Features
- Add food items and their calorie values
- View your total daily calories
- Visualize your progress with a pie chart
- Reset your daily calories

## Tech Stack
- **Frontend:** Streamlit, Plotly
- **Backend:** FastAPI

## Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/MohammadaminAlbooyeh/calorie_tracker.git
cd calorie_tracker
```

### 2. Install Dependencies
Install all required Python packages:
```bash
pip install -r requirements.txt
```

### 3. Run the FastAPI Backend
```bash
cd backend
uvicorn main:app --reload
```
The backend will be available at `http://127.0.0.1:8000`.

### 4. Run the Streamlit Frontend
Open a new terminal and run:
```bash
cd frontend
streamlit run app.py
```
The app will open in your browser.

## Usage
1. Enter the food item and its calorie value, then click **Add Entry**.
2. View your total calories and a pie chart of your progress.
3. Click **Reset Daily Calories** to start a new day.

## Project Structure
```
calorie_tracker/
├── backend/
│   └── main.py         # FastAPI backend
├── frontend/
│   └── app.py          # Streamlit frontend
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

## License
MIT
