# 🎢 FunFair AI: Ride Wait Time Predictor

**Role:** AI Engineer Take-Home Challenge  
**Status:** Completed

## 🧠 Overview
This project is an AI-powered application that predicts queue wait times for funfair rides. By analyzing factors like **weather, time of day, and day of the week**, the system helps visitors plan their trip to avoid long lines.

The solution includes:
1.  **Data Simulation Engine:** A Python script to generate realistic synthetic data based on park dynamics.
2.  **Machine Learning Pipeline:** A Random Forest model to predict wait times (MAE: ~4 minutes).
3.  **Interactive Dashboard:** A Streamlit web app for real-time predictions.

## 🚀 How to Run

### 1. Prerequisites
Ensure you have Python installed.

```bash
# Clone the repository (if applicable) or unzip the folder
cd funfair-wait-predictor

# Install dependencies
pip install -r requirements.txt

# Run the app
python -m streamlit run app/main.py