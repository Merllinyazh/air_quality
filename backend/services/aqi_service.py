from services.aqi_in_service import fetch_aqi_in
from services.openaq_service import fetch_openaq
from services.geo_service import fetch_by_geo
from services.ml_service import predict_aqi, is_model_trained
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


def is_valid(data):
    """Check if AQI data is usable"""
    return (
        data
        and isinstance(data, dict)
        and data.get("pm25") is not None
    )


def get_realtime_aqi(city):
    # 1️⃣ AQI.IN (LIVE)
    try:
        data = fetch_aqi_in(city)
        if is_valid(data):
            data["source"] = "AQI.IN"
            data["data_type"] = "live"
            data["category"] = calculate_category(data["pm25"])
            return data
    except Exception as e:
        print(f"[AQI.IN] Failed for {city}: {e}")

    # 2️⃣ OpenAQ
    try:
        data = fetch_openaq(city)
        if is_valid(data):
            data["source"] = "OpenAQ"
            data["data_type"] = "measured"
            data["category"] = calculate_category(data["pm25"])
            return data
    except Exception as e:
        print(f"[OpenAQ] Failed for {city}: {e}")

    # 3️⃣ Geo-based AQI
    try:
        data = fetch_by_geo(city)
        if is_valid(data):
            data["source"] = "Geo AQI"
            data["data_type"] = "estimated"
            data["category"] = calculate_category(data["pm25"])
            return data
    except Exception as e:
        print(f"[Geo] Failed for {city}: {e}")

    # 4️⃣ ML fallback (FORCED if enabled)
    if Config.ENABLE_ML_FALLBACK:
        try:
            if is_model_trained():
                # Safe proxy features
                features = [80, 120, 1.0, 25, 10, 35]
                pm25 = predict_aqi(features)

                if pm25 is not None:
                    data = {
                        "pm25": float(pm25),
                        "pm10": float(pm25) + 20,
                        "co": None,
                        "no2": None,
                        "so2": None,
                        "o3": None,
                        "source": "ML Model",
                        "data_type": "predicted"
                    }
                    data["category"] = calculate_category(data["pm25"])
                    return data
        except Exception as e:
            print(f"[ML] Failed for {city}: {e}")

    # ❌ Only if EVERYTHING fails
    return None
