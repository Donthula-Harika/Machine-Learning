# extract.py
import os
import json
import time
import logging
import requests
from datetime import datetime

BASE_URL = "https://air-quality-api.open-meteo.com/v1/air-quality"

CITIES = {
    "Delhi": (28.7041, 77.1025),
    "Mumbai": (19.0760, 72.8777),
    "Bengaluru": (12.9716, 77.5946),
    "Hyderabad": (17.3850, 78.4867),
    "Kolkata": (22.5726, 88.3639)
}

PARAMS = "pm10,pm2_5,carbon_monoxide,nitrogen_dioxide,ozone,sulphur_dioxide,uv_index"

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

def extract():
    os.makedirs("data/raw", exist_ok=True)
    saved_files = []
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")

    for city, (lat, lon) in CITIES.items():
        params = {
            "latitude": lat,
            "longitude": lon,
            "hourly": PARAMS
        }

        for attempt in range(3):
            try:
                resp = requests.get(BASE_URL, params=params, timeout=10)
                resp.raise_for_status()
                data = resp.json()

                file_path = f"data/raw/{city.lower()}_raw_{timestamp}.json"
                with open(file_path, "w") as f:
                    json.dump(data, f, indent=2)

                saved_files.append(file_path)
                logging.info(f"Saved data for {city}")
                break

            except Exception as e:
                logging.error(f"{city} | Attempt {attempt+1} failed: {e}")
                time.sleep(2)

    return saved_files

if __name__ == "__main__":
    extract()
