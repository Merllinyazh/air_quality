import requests
from config import Config

WAQI_BASE_URL = "https://api.waqi.info"

# Add as many Tamil Nadu cities as you want here
CITY_COORDINATES = {
    "madurai": (9.9252, 78.1198),
    "trichy": (10.7905, 78.7047),
    "tirunelveli": (8.7139, 77.7567),
    "theni": (10.0104, 77.4768),
    "thoothukudi": (8.7642, 78.1348),
    "vellore": (12.9165, 79.1325),
    "erode": (11.3410, 77.7172),
    "karur": (10.9601, 78.0766)
}


def fetch_by_geo(city):
    """
    Fetch AQI from the nearest monitoring station using latitude & longitude.
    Returns None if no station data is available.
    """

    city = city.lower()

    if city not in CITY_COORDINATES:
        return None

    lat, lon = CITY_COORDINATES[city]

    try:
        url = f"{WAQI_BASE_URL}/feed/geo:{lat};{lon}/?token={Config.AQI_API_KEY}"
        response = requests.get(url, timeout=10)
        data = response.json()

        if data.get("status") != "ok":
            return None

        iaqi = data["data"].get("iaqi")
        if not iaqi or "pm25" not in iaqi:
            return None

        return {
            "pm25": iaqi["pm25"]["v"],
            "pm10": iaqi.get("pm10", {}).get("v"),
            "co": iaqi.get("co", {}).get("v"),
            "no2": iaqi.get("no2", {}).get("v"),
            "so2": iaqi.get("so2", {}).get("v"),
            "o3": iaqi.get("o3", {}).get("v"),
            "source": "Nearest AQI Station",
            "data_type": "estimated"
        }

    except Exception as e:
        print("Geo AQI error:", e)
        return None
