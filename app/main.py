import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px

# --- SETUP & CONFIG ---
st.set_page_config(page_title="FunFair Predictor", page_icon="🎢", layout="wide")

# Map User-Friendly Names to Ride IDs (Must match training data!)
RIDE_MAPPING = {
    "Mega Coaster": "R_001",
    "Ferris Wheel": "R_002",
    "Bumper Cars": "R_003",
    "Haunted House": "R_004"
}

# --- LOAD MODEL ---
@st.cache_resource
def load_model():
    # Helper to load model efficiently
    try:
        return joblib.load('models/wait_time_model.pkl')
    except FileNotFoundError:
        st.error("Model not found! Please run the training notebook first.")
        return None

model = load_model()

# --- SIDEBAR INPUTS ---
st.sidebar.header("🎟️ Plan Your Visit")

# 1. Select Ride
selected_ride_name = st.sidebar.selectbox("Choose a Ride", list(RIDE_MAPPING.keys()))
ride_id = RIDE_MAPPING[selected_ride_name]

# 2. Select Time
selected_hour = st.sidebar.slider("Time of Day", min_value=10, max_value=22, value=12, step=1, format="%d:00")

# 3. Select Weather
selected_weather = st.sidebar.selectbox("Current Weather", ["Sunny", "Cloudy", "Rainy"])

# 4. Select Day Type
day_type = st.sidebar.radio("Day Type", ["Weekday", "Weekend"])
is_weekend = 1 if day_type == "Weekend" else 0

# --- MAIN PAGE ---
st.title("🎢 FunFair Ride Wait Predictor")
st.markdown("Use AI to predict queue times and plan your day better.")

# --- PREDICTION LOGIC ---
if st.sidebar.button("🔮 Predict Wait Time"):
    if model:
        # 1. Prepare Input Data
        # We must use the exact same column names as training
        input_data = pd.DataFrame([{
            'ride_id': ride_id,
            'weather': selected_weather,
            'hour_of_day': selected_hour,
            'is_weekend': is_weekend
        }])

        # 2. Make Prediction
        prediction = model.predict(input_data)[0]
        wait_time = int(prediction)

        # 3. Display Result
        col1, col2 = st.columns([1, 2])
        
        with col1:
            # Color logic based on wait time
            if wait_time < 15:
                color = "green"
                status = "Fast Lane! 🟢"
            elif wait_time < 45:
                color = "orange"
                status = "Moderate Wait 🟡"
            else:
                color = "red"
                status = "Long Queue 🔴"

            st.markdown(f"### Estimated Wait:")
            st.markdown(f"<h1 style='color:{color}'>{wait_time} min</h1>", unsafe_allow_html=True)
            st.write(f"**Status:** {status}")

        # --- BONUS: TREND CHART ---
        with col2:
            st.subheader(f"📅 Daily Trend for {selected_ride_name}")
            
            # Generate predictions for the WHOLE day (10am - 10pm) to show a curve
            hours = list(range(10, 23))
            trend_data = pd.DataFrame({
                'ride_id': [ride_id] * len(hours),
                'weather': [selected_weather] * len(hours),
                'hour_of_day': hours,
                'is_weekend': [is_weekend] * len(hours)
            })
            
            # Batch predict
            trend_preds = model.predict(trend_data)
            trend_df = pd.DataFrame({'Hour': hours, 'Wait Time': trend_preds})
            
            # Plot
            fig = px.line(trend_df, x='Hour', y='Wait Time', markers=True, 
                          title=f"Wait Time Curve ({selected_weather}, {day_type})")
            fig.update_layout(xaxis_title="Hour of Day", yaxis_title="Wait Time (min)")
            
            # Highlight the selected hour
            fig.add_vline(x=selected_hour, line_dash="dash", line_color="red", annotation_text="Selected Time")
            
            st.plotly_chart(fig, use_container_width=True)

else:
    st.info("👈 Adjust the inputs in the sidebar and click **Predict**!")