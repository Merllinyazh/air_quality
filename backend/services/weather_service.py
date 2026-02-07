import requests

CITY_COORDS = {
    # Major cities
    "chennai": (13.0827, 80.2707),
    "coimbatore": (11.0168, 76.9558),
    "madurai": (9.9252, 78.1198),
    "tiruchirappalli": (10.7905, 78.7047),
    "salem": (11.6643, 78.1460),
    "tirunelveli": (8.7139, 77.7567),
    "thoothukudi": (8.7642, 78.1348),
    "vellore": (12.9165, 79.1325),
    "erode": (11.3410, 77.7172),
    "dindigul": (10.3673, 77.9803),
    "thanjavur": (10.7870, 79.1378),
    "cuddalore": (11.7447, 79.7680),
    "nagapattinam": (10.7672, 79.8449),
    "karur": (10.9601, 78.0766),
    "namakkal": (11.2194, 78.1677),
    "krishnagiri": (12.5277, 78.2140),
    "dharmapuri": (12.1211, 78.1582),
    "kallakurichi": (11.7404, 78.9639),
    "ranipet": (12.9476, 79.3320),
    "tirupattur": (12.4953, 78.5670),
    "chengalpattu": (12.6847, 79.9836),
    "kanchipuram": (12.8342, 79.7036),
    "tiruvallur": (13.1430, 79.9080),
    "tiruvannamalai": (12.2253, 79.0747),
    "viluppuram": (11.9401, 79.4861),
    "perambalur": (11.2333, 78.8667),
    "ariyalur": (11.1385, 79.0756),
    "pudukkottai": (10.3813, 78.8214),
    "sivaganga": (9.8470, 78.4836),
    "ramanathapuram": (9.3716, 78.8307),
    "virudhunagar": (9.5680, 77.9624),
    "tenkasi": (8.9596, 77.3152),
    "the nilgiris": (11.4064, 76.6932),
    "kanyakumari": (8.0883, 77.5385),
    "mayiladuthurai": (11.1035, 79.6550)
}
def get_weather(city):
    city = city.lower().strip()

    if city not in CITY_COORDS:
        return {
            "status": "unavailable",
            "message": "Weather data not available for this city"
        }

    lat, lon = CITY_COORDS[city]

    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        "&current_weather=true"
        "&hourly=relativehumidity_2m,pressure_msl"
    )

    res = requests.get(url, timeout=10).json()

    current = res.get("current_weather", {})
    hourly = res.get("hourly", {})

    return {
        "temperature": current.get("temperature"),
        "wind_speed": current.get("windspeed"),
        "pressure": hourly.get("pressure_msl", [None])[0],
        "humidity": hourly.get("relativehumidity_2m", [None])[0],
        "weather_source": "Open-Meteo",
        "data_type": "measured"
    }
