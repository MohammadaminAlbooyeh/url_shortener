# app.py for Streamlit Frontend
import streamlit as st
import requests
import plotly.graph_objects as go

# --- Configuration ---
FASTAPI_BASE_URL = "http://127.0.0.1:8000" # Ensure this matches your FastAPI server address
MAX_DAILY_CALORIES = 2000

# --- Functions to interact with FastAPI ---
def add_calorie_entry_to_backend(item: str, calories: int):
    """Sends a new calorie entry to the FastAPI backend."""
    try:
        response = requests.post(
            f"{FASTAPI_BASE_URL}/add_calorie_entry/",
            json={"item": item, "calories": calories}
        )
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the backend API. Please ensure FastAPI is running.")
        return None
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred while adding entry: {e}")
        return None

def get_total_calories_from_backend():
    """Retrieves the current total calories from the FastAPI backend."""
    try:
        response = requests.get(f"{FASTAPI_BASE_URL}/get_total_calories/")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the backend API. Please ensure FastAPI is running.")
        return None
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred while fetching total calories: {e}")
        return None

def reset_calories_in_backend():
    """Resets the calorie tracker in the FastAPI backend."""
    try:
        response = requests.post(f"{FASTAPI_BASE_URL}/reset_calories/")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the backend API. Please ensure FastAPI is running.")
        return None
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred while resetting calories: {e}")
        return None

# --- Streamlit UI ---
st.set_page_config(
    page_title="Daily Calorie Tracker",
    layout="centered",
    initial_sidebar_state="auto"
)

st.title("Daily Calorie Tracker 🍎")
st.markdown("Track your daily calorie intake and visualize your progress!")

# --- Input Form ---
st.header("Add New Calorie Entry")
with st.form("calorie_entry_form"):
    item_name = st.text_input("Item Name", placeholder="e.g., Apple, Chicken Salad")
    calories_input = st.number_input("Calories", min_value=0, step=10, value=0)
    submitted = st.form_submit_button("Add Entry")

    if submitted:
        if item_name and calories_input >= 0:
            result = add_calorie_entry_to_backend(item_name, calories_input)
            if result:
                st.success(f"Added {calories_input} calories for {item_name}!")
                st.rerun() # Rerun to update the display
        else:
            st.warning("Please enter both item name and calories.")

# --- Display Current Total and Chart ---
st.header("Your Daily Summary")

# Fetch current total calories
summary = get_total_calories_from_backend()
if summary:
    total_calories = summary.get("total_calories", 0)
    st.metric(label="Total Calories Consumed", value=f"{total_calories} kcal")

    # Calculate remaining/over calories
    remaining_calories = MAX_DAILY_CALORIES - total_calories
    if remaining_calories >= 0:
        st.info(f"You have {remaining_calories} kcal remaining for today.")
    else:
        st.error(f"You are {abs(remaining_calories)} kcal over your daily limit!")

    # --- Pie Chart Visualization ---
    st.subheader("Calorie Breakdown")

    # Determine colors for the pie chart
    if total_calories <= MAX_DAILY_CALORIES:
        consumed_color = "#4CAF50"  # Green for within limit
        remaining_color = "#E0E0E0" # Light grey for remaining
        data = [
            go.Pie(
                labels=["Consumed", "Remaining"],
                values=[total_calories, max(0, remaining_calories)],
                marker_colors=[consumed_color, remaining_color],
                hole=0.4, # Donut chart
                name="Daily Calories"
            )
        ]
    else:
        # If over limit, show consumed vs. over limit
        consumed_color = "#FFC107" # Orange for consumed up to limit
        over_limit_color = "#F44336" # Red for over limit
        data = [
            go.Pie(
                labels=["Consumed (up to limit)", "Over Limit"],
                values=[MAX_DAILY_CALORIES, abs(remaining_calories)],
                marker_colors=[consumed_color, over_limit_color],
                hole=0.4, # Donut chart
                name="Daily Calories"
            )
        ]

    # Add a central text annotation for total calories
    layout = go.Layout(
        title_text=f"Daily Calorie Intake (Max: {MAX_DAILY_CALORIES} kcal)",
        annotations=[dict(text=f'{total_calories} kcal', x=0.5, y=0.5, font_size=20, showarrow=False)]
    )

    fig = go.Figure(data=data, layout=layout)
    fig.update_traces(hoverinfo="label+percent", textinfo="value", textfont_size=15)
    st.plotly_chart(fig, use_container_width=True)

# --- Reset Button ---
st.markdown("---")
if st.button("Reset Daily Calories"):
    reset_result = reset_calories_in_backend()
    if reset_result:
        st.success("Daily calories have been reset!")
        st.rerun() # Rerun to update the display

# --- Instructions ---
st.sidebar.header("How to Use")
st.sidebar.markdown("""
1.  **Run the FastAPI Backend:**
    * Save the first code block as `main.py`.
    * Open your terminal/command prompt.
    * Navigate to the directory where you saved `main.py`.
    * Run: `pip install fastapi uvicorn`
    * Then run: `uvicorn main:app --reload`
    * Keep this terminal window open.

2.  **Run the Streamlit Frontend:**
    * Save the second code block as `app.py`.
    * Open a new terminal/command prompt.
    * Navigate to the directory where you saved `app.py`.
    * Run: `pip install streamlit requests plotly`
    * Then run: `streamlit run app.py`
    * This will open the Streamlit app in your web browser.

3.  **Track Calories:**
    * Enter the item name and its calorie count in the Streamlit app.
    * Click "Add Entry".
    * The total calories and the pie chart will update automatically.
    * The pie chart will turn red if you exceed 2000 kcal.
    * Click "Reset Daily Calories" to start fresh for a new day.
""")
