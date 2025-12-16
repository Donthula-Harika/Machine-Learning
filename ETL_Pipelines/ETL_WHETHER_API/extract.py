# extract.py
import json
from datetime import datetime
from pathlib import Path
import requests
from dotenv import load_dotenv
import os
 
load_dotenv()
  
BASE_DIR = Path(__file__).resolve().parents[0]  #purpose: get the base directory of the project
                    #__file__ → path of the current script.
                    # .resolve() → absolute path.
                    # .parents[0] → directory containing the script.
                    # This becomes your project root for this script.
RAW_DIR = BASE_DIR / "data" / "raw"
                    # Builds a folder path like:
                    # project/data/raw
RAW_DIR.mkdir(parents=True, exist_ok=True) # Ensure the raw data directory exists
 
LAT = os.getenv("LAT", "17.3850")
LON = os.getenv("LON", "78.4867")
FORECAST_DAYS = int(os.getenv("FORECAST_DAYS", "1"))
 
def extract_weather_data(lat: str = LAT, lon: str = LON, days: int = FORECAST_DAYS):
    """
    Call Open-Meteo API and store raw JSON to data/raw/.
    Returns path to saved file.
    """
    url = "https://api.open-meteo.com/v1/forecast"   #Base URL of the weather API.
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "temperature_2m,relativehumidity_2m,windspeed_10m",
        "forecast_days": days,
        "timezone": "auto"
    }
 
    print(f"⏳ Requesting weather data for lat={lat}, lon={lon}, days={days} ...")
    resp = requests.get(url, params=params, timeout=30)  # Send GET request to the API with parameters and a timeout of 30 seconds.
    resp.raise_for_status()
    data = resp.json()  # Parse the JSON response from the API.
 
     # Save the JSON payload to a timestamped file in the raw data directory.
     # Filename format: weather_YYYYMMDD_HHMMSS.json
     # Example: weather_20231005_153045.json
 
    filename = RAW_DIR / f"weather_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    filename.write_text(json.dumps(data, indent=2)) # Write the JSON data to the file with pretty formatting.
    print(f"✅ Extracted weather data and saved to: {filename}")
    return str(filename)
 
if __name__ == "__main__":
    extract_weather_data() 
 
 