from services.aqi_in_service import fetch_aqi_in
from services.openaq_service import fetch_openaq
from services.geo_service import fetch_by_geo
from services.ml_service import predict_aqi, is_model_trained
from config import Config


def calculate_category(pm25):
    if pm25 <= 50: return "Good"
    elif pm25 <= 100: return "Satisfactory"
    elif pm25 <= 200: return "Moderate"
    elif pm25 <= 300: return "Poor"
    return "Severe"


def get_realtime_aqi(city):
    # 1️⃣ AQI.IN (LIVE — MOST IMPORTANT)
    data = fetch_aqi_in(city)

    # 2️⃣ OpenAQ
    if not data:
        data = fetch_openaq(city)

    # 3️⃣ Geo-based AQI
    if not data:
        data = fetch_by_geo(city)

    # 4️⃣ ML fallback (ONLY if trained)
    if not data and Config.ENABLE_ML_FALLBACK and is_model_trained():
        features = [80, 120, 1.0, 25, 10, 35]  # safe proxy
        pm25 = predict_aqi(features)

        if pm25:
            data = {
                "pm25": pm25,
                "pm10": pm25 + 20,
                "co": None,
                "no2": None,
                "so2": None,
                "o3": None,
                "source": "ML Model",
                "data_type": "predicted"
            }

    if not data:
        return None

    data["category"] = calculate_category(data["pm25"])
    return data
