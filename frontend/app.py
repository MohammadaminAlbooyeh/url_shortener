import streamlit as st
import requests
import plotly.graph_objects as go
from food_calaries import FOOD_CALORIES_DATABASE # Assuming this is in frontend/food_calaries.py
import colorsys
import pandas as pd
from datetime import date # Import date object

FASTAPI_BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Daily Calorie Tracker", layout="wide")
st.title("Daily Calorie Tracker 🍎")
st.markdown("Track your daily calorie intake and visualize your progress!")

# --- Custom CSS to make the progress bar thicker ---
st.markdown(
    """
    <style>
    /* Target the Streamlit progress bar container */
    .stProgress > div > div > div > div {
        background-color: #4CAF50; /* Green color for the filled part */
        height: 25px; /* Adjust this value for desired thickness */
        border-radius: 0.5rem; /* Keep rounded corners if desired */
    }
    /* Target the unfilled part of the progress bar */
    .stProgress > div > div > div {
        background-color: #f0f2f6; /* Light gray for the background */
        height: 25px; /* Must match the filled part's height */
        border-radius: 0.5rem; /* Keep rounded corners if desired */
    }
    </style>
    """,
    unsafe_allow_html=True
)
# --- End Custom CSS ---

# Initialize session state for food and unit selection if not already present
if 'selected_food_item' not in st.session_state:
    st.session_state.selected_food_item = list(FOOD_CALORIES_DATABASE.keys())[0]
if 'selected_unit_index' not in st.session_state:
    st.session_state.selected_unit_index = 0
if 'quantity_input_value' not in st.session_state:
    initial_food = list(FOOD_CALORIES_DATABASE.keys())[0]
    initial_unit_info = FOOD_CALORIES_DATABASE[initial_food][0]
    st.session_state.quantity_input_value = str(initial_unit_info["default_quantity_input"])

# New: Initialize selected_date in session state
if 'selected_date' not in st.session_state:
    st.session_state.selected_date = date.today()

# --- Layout: 2 columns side by side ---
left_col, right_col = st.columns([1, 2])

with left_col:
    st.header("Add Food Entry")

    # Callback to reset unit selection and quantity when food item changes
    def on_food_change():
        st.session_state.selected_unit_item = st.session_state.selected_food_item
        st.session_state.selected_unit_index = 0
        first_unit_info = FOOD_CALORIES_DATABASE[st.session_state.selected_food_item][0]
        st.session_state.quantity_input_value = str(first_unit_info["default_quantity_input"])

    # Food Item Selectbox - MOVED OUTSIDE THE FORM
    food_item = st.selectbox(
        "Select food item",
        list(FOOD_CALORIES_DATABASE.keys()),
        key='selected_food_item',
        on_change=on_food_change
    )

    # Now, the form starts here
    with st.form("food_entry_form"):
        available_units_for_food = FOOD_CALORIES_DATABASE.get(food_item, [])
        unit_names = [unit_info["unit_name"] for unit_info in available_units_for_food]

        selected_unit_name = st.selectbox(
            "Select unit",
            unit_names,
            index=st.session_state.selected_unit_index,
            key='selected_unit_index_in_form'
        )

        selected_unit_info = available_units_for_food[st.session_state.selected_unit_index]
        calories_per_unit = selected_unit_info["calories_per_unit_value"]
        is_discrete = selected_unit_info["is_discrete_input"]

        quantity = None
        quantity_error = False

        if is_discrete:
            try:
                current_quantity_value = int(float(st.session_state.quantity_input_value))
            except ValueError:
                current_quantity_value = selected_unit_info["default_quantity_input"]

            quantity = st.number_input(
                f"Enter quantity ({selected_unit_name})",
                min_value=1,
                value=current_quantity_value,
                step=1,
                key="discrete_quantity"
            )
            st.session_state.quantity_input_value = str(quantity)

        else:
            quantity_str = st.text_input(
                f"Enter quantity ({selected_unit_name})",
                value=str(st.session_state.quantity_input_value),
                key="continuous_quantity"
            )
            try:
                quantity = float(quantity_str)
                if quantity < 0:
                    st.error("Quantity cannot be negative.")
                    quantity_error = True
            except ValueError:
                st.error("Please enter a valid number for quantity.")
                quantity_error = True
            st.session_state.quantity_input_value = quantity_str

        calories = 0
        if quantity is not None and not quantity_error:
            calories = int(quantity * calories_per_unit)
        else:
            calories = 0

        st.write(f"**Estimated Calories:** {calories} kcal")

        submitted = st.form_submit_button("Add Entry", disabled=quantity_error)
        if submitted:
            if quantity_error:
                st.error("Please correct the quantity input before submitting.")
            else:
                try:
                    response = requests.post(
                        f"{FASTAPI_BASE_URL}/add_calorie_entry/",
                        json={"item": food_item, "calories": calories, "unit": selected_unit_name}
                    )
                    response.raise_for_status()
                    st.success(f"Added {food_item} ({calories} kcal) to your daily log ({quantity} {selected_unit_name}).")
                    # No need to reset selected_date as it defaults to today
                    st.session_state.selected_food_item = list(FOOD_CALORIES_DATABASE.keys())[0]
                    st.session_state.selected_unit_index = 0
                    first_food_default_unit_info = FOOD_CALORIES_DATABASE[st.session_state.selected_food_item][0]
                    st.session_state.quantity_input_value = str(first_food_default_unit_info["default_quantity_input"])

                    st.experimental_rerun()
                except Exception as e:
                    st.error(f"Failed to add entry: {e}")

# === Right Column: Combined Layout ===
with right_col:
    st.header("Daily Overview") # Changed header for clarity

    # Date Selector
    selected_date = st.date_input(
        "View entries for:",
        value=st.session_state.selected_date,
        key='selected_date'
    )

    # --- Fetch entries and summary based on selected_date ---
    try:
        # Pass the selected date to the backend API calls
        entries_response = requests.get(f"{FASTAPI_BASE_URL}/get_entries/?date={selected_date.isoformat()}")
        entries_response.raise_for_status()
        entries = entries_response.json()

        summary_response = requests.get(f"{FASTAPI_BASE_URL}/get_total_calories/?date={selected_date.isoformat()}")
        summary_response.raise_for_status()
        summary = summary_response.json()

        total_calories = summary.get("total_calories", 0)
        max_daily = summary.get("max_daily_calories", 2000)
    except Exception as e:
        st.error(f"Could not fetch data for {selected_date}: {e}")
        entries = []
        total_calories = 0
        max_daily = 2000

    # Define common functions for colors (moved here to ensure scope)
    def get_n_colors(n):
        hues = [i / n for i in range(n)]
        color_list = []
        for h in hues:
            r, g, b = colorsys.hsv_to_rgb(h, 0.6, 0.9)
            color_list.append(f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}")
        return color_list

    # --- EMOJI MAPPING ---
    FOOD_EMOJIS = {
        "apple": "🍎", "banana": "🍌", "orange": "🍊", "pear": "🍐", "grapes": "🍇",
        "strawberry": "🍓", "blueberry": "🫐", "watermelon": "🍉", "pineapple": "🍍", "kiwi": "🥝",
        "mango": "🥭", "peach": "🍑", "plum": " Plum", "cherry": "🍒", "apricot": " Apricot",
        "carrot": "🥕", "potato": "🥔", "tomato": "🍅", "cucumber": "🥒", "lettuce": "🥬",
        "broccoli": "🥦", "cauliflower": " Cauliflower", "spinach": "🥬", "onion": "🧅", "garlic": "🧄",
        "egg": "🥚", "chicken breast": "🍗", "beef": "🥩", "my beef": "🥩", "lamb": "🐑", "salmon": "🐟",
        "tuna": "🐟", "shrimp": "🦐", "rice": "🍚", "bread": "🍞", "pasta": "🍝",
        "pizza": "🍕", "hamburger": "🍔", "hot dog": "🌭", "cheese": "🧀", "milk": "🥛",
        "yogurt": "🍦", "butter": "🧈", "olive oil": "🫒", "sugar": " cubes", "honey": "🍯",
        "almonds": "🌰", "walnuts": "🌰", "peanut butter": "🧈", "potato chips": "🍟", "chocolate": "🍫",
        "ice cream": "🍦", "cookie": "🍪", "cake": "🍰",
        "default": "🍽️"
    }
    # --- END EMOJI MAPPING ---

    # Create two columns within the right column for chart and summary
    chart_col, summary_details_col = st.columns([2, 1])

    with chart_col:
        # Update food_labels to exclude unit information
        food_labels = [e['item'] for e in entries]
        food_values = [e['calories'] for e in entries]
        food_colors = get_n_colors(len(food_labels)) if food_labels else ["#4CAF50"]

        if food_labels and sum(food_values) > 0:
            fig = go.Figure(data=[go.Pie(
                labels=food_labels,
                values=food_values,
                marker_colors=food_colors,
                hole=0.4,
                name="Foods"
            )])
            fig.update_layout(
                title_text=f"Total: {total_calories} kcal",
                annotations=[dict(text=f'{total_calories} kcal', x=0.5, y=0.5, font_size=20, showarrow=False)]
            )
            fig.update_traces(hoverinfo="label+percent", textinfo="value", textfont_size=15)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info(f"No foods added yet for {selected_date.strftime('%Y-%m-%d')}.") # Specific message for date

    with summary_details_col:
        st.subheader("Summary for Selected Date") # Changed header

        # --- Calorie Progress Bar (inside summary_details_col) ---
        progress_percentage = min(total_calories / max_daily, 1.0) if max_daily > 0 else 0
        remaining_calories = max_daily - total_calories

        st.markdown(
            f"""
            <div style="font-size: 1.1em; font-weight: bold; margin-bottom: 5px;">
                <span>Consumed: {total_calories} kcal</span><br>
                <span>Remaining: {max(0, remaining_calories)} kcal</span>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.progress(progress_percentage)

        if remaining_calories < 0:
            st.warning(f"You are {abs(remaining_calories)} kcal over your daily limit!")
        # --- End Calorie Progress Bar ---

        st.markdown("**What you ate on this day:**") # Changed header for clarity

        for i, entry in enumerate(entries):
            item_name = entry['item']
            calories_value = entry['calories']
            unit_display = entry.get('unit', '') # Still get unit to display if available

            emoji = FOOD_EMOJIS.get(item_name.lower(), FOOD_EMOJIS["default"])
            current_color = food_colors[i % len(food_colors)] if food_colors else "#4CAF50"

            st.markdown(
                f'<span style="display:inline-block;width:16px;height:16px;background:{current_color};'
                f'border-radius:3px;margin-right:8px;"></span> '
                f'<span style="font-size: 1.1em; font-weight: bold;">{emoji} {item_name}</span> '
                f'<span style="color:gray;">({calories_value} kcal - {unit_display})</span>', # Re-added unit here
                unsafe_allow_html=True
            )

    # Reset Button - Moved outside the sub-columns for better visibility
    st.write("---") # Separator

    # Reset button for the selected date
    if st.button(f"Reset Calories for {selected_date.strftime('%Y-%m-%d')}"):
        try:
            resp = requests.post(f"{FASTAPI_BASE_URL}/reset_calories/?date={selected_date.isoformat()}")
            resp.raise_for_status()
            st.success(f"Calories for {selected_date.strftime('%Y-%m-%d')} have been reset!")
            st.experimental_rerun()
        except Exception as e:
            st.error(f"Error resetting calories: {e}")

    st.write("---") # Another separator

    # Export Data Section
    st.subheader("Export Your Data")
    if st.button("Generate Full Calorie Log (CSV)"):
        try:
            export_response = requests.get(f"{FASTAPI_BASE_URL}/get_all_entries/")
            export_response.raise_for_status()
            all_entries = export_response.json()

            if all_entries:
                df = pd.DataFrame(all_entries)
                # Reorder columns for better readability and ensure date is first
                df = df[['date', 'item', 'calories', 'unit', 'id']] # 'id' last or drop it if not needed
                csv_data = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Download CSV",
                    data=csv_data,
                    file_name="calorie_log_full.csv",
                    mime="text/csv",
                    key='download_full_csv'
                )
                st.success("CSV generated!")
            else:
                st.info("No historical data to export yet.")
        except Exception as e:
            st.error(f"Error generating CSV: {e}")