from services.openaq_service import fetch_openaq
from services.geo_service import fetch_by_geo
from services.ml_service import predict_aqi
from config import Config


def calculate_category(pm25):
    if pm25 <= 50:
        return "Good"
    elif pm25 <= 100:
        return "Satisfactory"
    elif pm25 <= 200:
        return "Moderate"
    elif pm25 <= 300:
        return "Poor"
    return "Severe"


def get_realtime_aqi(city):
    """
    Hybrid AQI logic:
    1. OpenAQ (measured)
    2. Nearest AQI station (estimated)
    3. ML prediction (fallback)
    """

    data = fetch_openaq(city)

    if not data:
        data = fetch_by_geo(city)

    if not data and Config.ENABLE_ML_FALLBACK:
        data = predict_aqi(city)

    if not data:
        return None

    data["category"] = calculate_category(data["pm25"])
    return data
