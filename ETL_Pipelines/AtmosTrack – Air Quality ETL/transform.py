# transform.py
import os
import json
import pandas as pd

RAW_DIR = "data/raw"
STAGED_PATH = "data/staged/air_quality_transformed.csv"

def classify_aqi(pm25):
    if pm25 <= 50: return "Good"
    if pm25 <= 100: return "Moderate"
    if pm25 <= 200: return "Unhealthy"
    if pm25 <= 300: return "Very Unhealthy"
    return "Hazardous"

def transform():
    records = []

    for file in os.listdir(RAW_DIR):
        with open(os.path.join(RAW_DIR, file)) as f:
            data = json.load(f)

        city = file.split("_")[0].title()
        hourly = data.get("hourly", {})

        df = pd.DataFrame(hourly)
        df["city"] = city
        df["time"] = pd.to_datetime(df["time"])

        df["severity_score"] = (
            df["pm2_5"] * 5 +
            df["pm10"] * 3 +
            df["nitrogen_dioxide"] * 4 +
            df["sulphur_dioxide"] * 4 +
            df["carbon_monoxide"] * 2 +
            df["ozone"] * 3
        )

        df["aqi_category"] = df["pm2_5"].apply(classify_aqi)

        df["risk_flag"] = df["severity_score"].apply(
            lambda x: "High Risk" if x > 400 else "Moderate Risk" if x > 200 else "Low Risk"
        )

        df["hour"] = df["time"].dt.hour
        records.append(df)

    final_df = pd.concat(records)
    final_df = final_df.dropna(how="all", subset=[
        "pm10","pm2_5","carbon_monoxide","nitrogen_dioxide","sulphur_dioxide","ozone"
    ])

    os.makedirs("data/staged", exist_ok=True)
    final_df.to_csv(STAGED_PATH, index=False)
    return STAGED_PATH

if __name__ == "__main__":
    transform()
