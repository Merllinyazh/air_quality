from services.aqi_in_service import fetch_aqi_in
from services.openaq_service import fetch_openaq
from services.geo_service import fetch_by_geo
from services.ml_service import predict_aqi, is_model_trained
from services.aqi_calc import calculate_aqi_from_pollutants
from config import Config


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
            aqi_result = calculate_aqi_from_pollutants(data)

            data["source"] = "AQI.IN"
            data["data_type"] = "live"

            if aqi_result:
                data.update(aqi_result)
            else:
                data["aqi"] = None
                data["category"] = "Insufficient Data"

            return data
    except Exception as e:
        print(f"[AQI.IN] Failed for {city}: {e}")

    # 2️⃣ OpenAQ
    try:
        data = fetch_openaq(city)
        if is_valid(data):
            aqi_result = calculate_aqi_from_pollutants(data)

            data["source"] = "OpenAQ"
            data["data_type"] = "measured"

            if aqi_result:
                data.update(aqi_result)
            else:
                data["aqi"] = None
                data["category"] = "Insufficient Data"

            return data
    except Exception as e:
        print(f"[OpenAQ] Failed for {city}: {e}")

    # 3️⃣ Geo-based AQI
    try:
        data = fetch_by_geo(city)
        if is_valid(data):
            aqi_result = calculate_aqi_from_pollutants(data)

            data["source"] = "Geo AQI"
            data["data_type"] = "estimated"

            if aqi_result:
                data.update(aqi_result)
            else:
                data["aqi"] = None
                data["category"] = "Insufficient Data"

            return data
    except Exception as e:
        print(f"[Geo] Failed for {city}: {e}")

    # 4️⃣ ML fallback
    if Config.ENABLE_ML_FALLBACK:
        try:
            if is_model_trained():
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

                    aqi_result = calculate_aqi_from_pollutants(data)
                    if aqi_result:
                        data.update(aqi_result)
                    else:
                        data["aqi"] = None
                        data["category"] = "Insufficient Data"

                    return data
        except Exception as e:
            print(f"[ML] Failed for {city}: {e}")

    # ❌ Only if EVERYTHING fails
    return None
