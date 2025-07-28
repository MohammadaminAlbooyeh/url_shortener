import streamlit as st
import requests
import plotly.graph_objects as go
from food_calaries import FOOD_CALORIES_DATABASE
import colorsys

FASTAPI_BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Daily Calorie Tracker", layout="wide")
st.title("Daily Calorie Tracker 🍎")
st.markdown("Track your daily calorie intake and visualize your progress!")

# Initialize session state for food and unit selection if not already present
if 'selected_food_item' not in st.session_state:
    st.session_state.selected_food_item = list(FOOD_CALORIES_DATABASE.keys())[0]
if 'selected_unit_index' not in st.session_state:
    st.session_state.selected_unit_index = 0
if 'quantity_input_value' not in st.session_state:
    # Set initial quantity to the default for the very first food item's first unit
    initial_food = list(FOOD_CALORIES_DATABASE.keys())[0]
    initial_unit_info = FOOD_CALORIES_DATABASE[initial_food][0]
    st.session_state.quantity_input_value = str(initial_unit_info["default_quantity_input"])


# --- Layout: 2 columns side by side ---
left_col, right_col = st.columns([1, 2])

with left_col:
    st.header("Add Food Entry")

    # Callback to reset unit selection and quantity when food item changes
    def on_food_change():
        st.session_state.selected_unit_index = 0 # Reset to the first unit
        # Also reset quantity to the default for the new food's default unit
        first_unit_info = FOOD_CALORIES_DATABASE[st.session_state.selected_food_item][0]
        st.session_state.quantity_input_value = str(first_unit_info["default_quantity_input"])

    # Food Item Selectbox - MOVED OUTSIDE THE FORM
    food_item = st.selectbox(
        "Select food item",
        list(FOOD_CALORIES_DATABASE.keys()),
        key='selected_food_item', # Bind to session state
        on_change=on_food_change
    )

    # Now, the form starts here
    with st.form("food_entry_form"):
        # Get available units for the selected food item (from outside the form)
        available_units_for_food = FOOD_CALORIES_DATABASE.get(food_item, [])
        unit_names = [unit_info["unit_name"] for unit_info in available_units_for_food]

        # Unit Selectbox (inside the form)
        selected_unit_name = st.selectbox(
            "Select unit",
            unit_names,
            index=st.session_state.selected_unit_index, # Control with session state
            key='selected_unit_index_in_form' # Needs a different key if also used outside a form
                                                # For simplicity, keeping it inside and using session_state index
        )

        # Get the full info for the currently selected unit
        # We need to ensure we're getting the info based on the *currently selected index*
        selected_unit_info = available_units_for_food[st.session_state.selected_unit_index]
        calories_per_unit = selected_unit_info["calories_per_unit_value"]
        is_discrete = selected_unit_info["is_discrete_input"]
        default_quantity = selected_unit_info["default_quantity_input"] # Use this default for value if session state is empty

        # Conditional Quantity Input
        quantity = None
        quantity_error = False

        if is_discrete:
            # For discrete items (like apples), use number_input with step=1
            # Ensure the value is cast to int for discrete input
            try:
                current_quantity_value = int(st.session_state.quantity_input_value)
            except ValueError:
                current_quantity_value = default_quantity # Fallback if session state value is invalid for int

            quantity = st.number_input(
                f"Enter quantity ({selected_unit_name})",
                min_value=1,
                value=current_quantity_value,
                step=1,
                key="discrete_quantity"
            )
            st.session_state.quantity_input_value = str(quantity) # Keep session state updated

        else:
            # For continuous items (like milk/rice), use text_input for no +/- buttons
            quantity_str = st.text_input(
                f"Enter quantity ({selected_unit_name})",
                value=str(st.session_state.quantity_input_value), # Use current session state value
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
            st.session_state.quantity_input_value = quantity_str # Update session state to keep value in textbox

        calories = 0
        if quantity is not None and not quantity_error:
            calories = int(quantity * calories_per_unit)
        else:
            calories = 0 # Or some indicator that it's not calculable

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
                    # Reset inputs after successful submission for next entry
                    # This reruns the app, and the initial session state setup will handle defaults
                    st.session_state.selected_food_item = list(FOOD_CALORIES_DATABASE.keys())[0]
                    st.session_state.selected_unit_index = 0
                    first_food_default_unit_info = FOOD_CALORIES_DATABASE[st.session_state.selected_food_item][0]
                    st.session_state.quantity_input_value = str(first_food_default_unit_info["default_quantity_input"])

                    st.experimental_rerun()
                except Exception as e:
                    st.error(f"Failed to add entry: {e}")

# === Right Column: Daily Summary & Pie Chart ===
with right_col:
    st.header("Your Daily Summary")
    try:
        summary = requests.get(f"{FASTAPI_BASE_URL}/get_total_calories/").json()
        total_calories = summary.get("total_calories", 0)
        max_daily = summary.get("max_daily_calories", 2000)
        st.metric("Total Calories Consumed", f"{total_calories} kcal")
        remaining = max_daily - total_calories
        if remaining >= 0:
            st.info(f"You have {remaining} kcal remaining for today.")
        else:
            st.error(f"You are {abs(remaining)} kcal over your daily limit!")

        # Pie Chart & Breakdown
        st.subheader("Calorie Breakdown")
        try:
            entries = requests.get(f"{FASTAPI_BASE_URL}/get_entries/").json()
        except Exception:
            entries = []

        def get_n_colors(n):
            hues = [i / n for i in range(n)]
            color_list = []
            for h in hues:
                r, g, b = colorsys.hsv_to_rgb(h, 0.6, 0.9)
                color_list.append(f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}")
            return color_list

        food_labels = [f"{e['item']} ({e.get('unit', 'N/A')})" for e in entries]
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
                title_text=f"Food Breakdown (Total: {total_calories} kcal)",
                annotations=[dict(text=f'{total_calories} kcal', x=0.5, y=0.5, font_size=20, showarrow=False)]
            )
            fig.update_traces(hoverinfo="label+percent", textinfo="value", textfont_size=15)
            st.plotly_chart(fig, use_container_width=True)

            st.markdown("**What you ate today:**")
            for i, entry in enumerate(entries):
                label = entry['item']
                value = entry['calories']
                unit_display = entry.get('unit', '')
                # Ensure we have enough colors for the labels
                current_color = food_colors[i % len(food_colors)] if food_colors else "#4CAF50"

                st.markdown(
                    f'<span style="display:inline-block;width:16px;height:16px;background:{current_color};'
                    f'border-radius:3px;margin-right:8px;"></span> {label} '
                    f'<span style="color:gray;">({value} kcal - {unit_display})</span>',
                    unsafe_allow_html=True
                )
        else:
            st.info("No foods added yet.")

        # Reset Button
        if st.button("Reset Daily Calories"):
            try:
                resp = requests.post(f"{FASTAPI_BASE_URL}/reset_calories/")
                resp.raise_for_status()
                st.success("Daily calories have been reset!")
                st.experimental_rerun()
            except Exception as e:
                st.error(f"Error resetting calories: {e}")

    except Exception as e:
        st.error(f"Could not fetch summary: {e}")