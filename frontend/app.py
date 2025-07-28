import streamlit as st
import requests
import plotly.graph_objects as go
from food_calaries import FOOD_CALORIES_DATABASE
import colorsys

FASTAPI_BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Daily Calorie Tracker", layout="wide")
st.title("Daily Calorie Tracker 🍎")
st.markdown("Track your daily calorie intake and visualize your progress!")

# --- Layout: 2 columns side by side ---
left_col, right_col = st.columns([1, 2])

# === Left Column: Food Entry Form ===
with left_col:
    st.header("Add Food Entry")
    with st.form("food_entry_form"):
        food_item = st.selectbox("Select food item", list(FOOD_CALORIES_DATABASE.keys()))

        # Get the selected food's unit and calories per unit from the updated database
        selected_food_info = FOOD_CALORIES_DATABASE[food_item][0]
        input_unit = selected_food_info["input_unit"]
        calories_per_input_unit = selected_food_info["calories_per_input_unit"]

        # Display the unit dynamically next to the quantity input
        quantity = st.number_input(f"Enter quantity ({input_unit})", min_value=0.0, value=1.0, step=0.5)

        # Calculate estimated calories based on the new 'calories_per_input_unit'
        calories = int(quantity * calories_per_input_unit)

        st.write(f"**Estimated Calories:** {calories} kcal")

        submitted = st.form_submit_button("Add Entry")
        if submitted:
            try:
                # Send the unit information to the backend
                response = requests.post(
                    f"{FASTAPI_BASE_URL}/add_calorie_entry/",
                    json={"item": food_item, "calories": calories, "unit": input_unit}
                )
                response.raise_for_status()
                st.success(f"Added {food_item} ({calories} kcal) to your daily log.")
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
                title_text=f"Food Breakdown (Total: {total_calories} kcal)",
                annotations=[dict(text=f'{total_calories} kcal', x=0.5, y=0.5, font_size=20, showarrow=False)]
            )
            fig.update_traces(hoverinfo="label+percent", textinfo="value", textfont_size=15)
            st.plotly_chart(fig, use_container_width=True)

            st.markdown("**What you ate today:**")
            # Display item, calories, AND unit
            for entry in entries:
                label = entry['item']
                value = entry['calories']
                unit_display = entry.get('unit', '') # Use .get() in case older entries don't have 'unit'
                st.markdown(
                    f'<span style="display:inline-block;width:16px;height:16px;background:{food_colors[food_labels.index(label)]};'
                    f'border-radius:3px;margin-right:8px;"></span> {label} '
                    f'<span style="color:gray;">({value} kcal - {unit_display})</span>', # Added unit_display
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