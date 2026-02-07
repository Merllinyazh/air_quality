import requests

OPENAQ_BASE_URL = "https://api.openaq.org/v2/latest"

HEADERS = {
    "User-Agent": "AirQuality-College-Project",
    "Accept": "application/json"
}


def fetch_openaq(city):
    """
    Fetch measured AQI-related pollutant data from OpenAQ.
    Returns None if no usable data is found.
    """

    try:
        url = f"{OPENAQ_BASE_URL}?city={city}&limit=1"
        response = requests.get(url, headers=HEADERS, timeout=10)
        data = response.json()

        if not data.get("results"):
            return None

        measurements = data["results"][0].get("measurements", [])
        if not measurements:
            return None

        pm25 = None
        pm10 = None
        co = None
        no2 = None
        so2 = None
        o3 = None

        for m in measurements:
            param = m.get("parameter")
            value = m.get("value")

            if param == "pm25":
                pm25 = value
            elif param == "pm10":
                pm10 = value
            elif param == "co":
                co = value
            elif param == "no2":
                no2 = value
            elif param == "so2":
                so2 = value
            elif param == "o3":
                o3 = value

        # PM2.5 is mandatory to calculate AQI
        if pm25 is None:
            return None

        return {
            "pm25": pm25,
            "pm10": pm10,
            "co": co,
            "no2": no2,
            "so2": so2,
            "o3": o3,
            "source": "OpenAQ",
            "data_type": "measured"
        }

    except Exception as e:
        print("OpenAQ error:", e)
        return None
