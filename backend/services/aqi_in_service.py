import requests
from config import Config

BASE_URL = "https://api.waqi.info"


def fetch_aqi_in(city):
    """
    Fetch LIVE AQI data from AQI.IN / WAQI for a given city.
    Returns None if data is unavailable or incomplete.
    """

    if not Config.AQI_API_KEY:
        print("❌ AQI_API_KEY not set")
        return None

    try:
        url = f"{BASE_URL}/feed/{city}/?token={Config.AQI_API_KEY}"
        response = requests.get(url, timeout=10)
        data = response.json()

        # Status check
        if data.get("status") != "ok":
            return None

        station_data = data.get("data", {})
        iaqi = station_data.get("iaqi")

        # PM2.5 is mandatory
        if not iaqi or "pm25" not in iaqi:
            return None

        return {
            "pm25": iaqi["pm25"]["v"],
            "pm10": iaqi.get("pm10", {}).get("v"),
            "co": iaqi.get("co", {}).get("v"),
            "no2": iaqi.get("no2", {}).get("v"),
            "so2": iaqi.get("so2", {}).get("v"),
            "o3": iaqi.get("o3", {}).get("v"),
            "source": "AQI.IN",
            "data_type": "live"
        }

    except requests.exceptions.RequestException as e:
        print("AQI.IN request failed:", e)
        return None
    except Exception as e:
        print("AQI.IN unexpected error:", e)
        return None
