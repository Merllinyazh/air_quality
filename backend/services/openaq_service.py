import requests

OPENAQ_BASE_URL = "https://api.openaq.org/v2/latest"

HEADERS = {
    "User-Agent": "AirQuality-College-Project",
    "Accept": "application/json"
}


def fetch_openaq(city):
    try:
        url = f"{OPENAQ_BASE_URL}?limit=1&country=IN&city={city}"
        response = requests.get(url, headers=HEADERS, timeout=10)
        data = response.json()

        if not data.get("results"):
            return None

        measurements = data["results"][0].get("measurements", [])
        if not measurements:
            return None

        pm25 = next((m["value"] for m in measurements if m["parameter"] == "pm25"), None)

        if pm25 is None:
            return None

        return {
            "pm25": pm25,
            "pm10": None,
            "co": None,
            "no2": None,
            "so2": None,
            "o3": None,
            "source": "OpenAQ",
            "data_type": "measured"
        }

    except Exception:
        return None