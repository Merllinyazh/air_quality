from services.aqi_in_service import fetch_aqi_in
from services.openaq_service import fetch_openaq
from services.geo_service import fetch_by_geo
from services.ml_service import (
    predict_current_aqi,
    forecast_short_term,
    forecast_long_term,
    is_model_trained,
    train_model,
    aqi_category
)
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

    data = None  # Important: define early to avoid reference error

    # 1️⃣ AQI.IN
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

    # 3️⃣ Geo-based
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

    # 4️⃣ DISTRICT ML FALLBACK
    if Config.ENABLE_ML_FALLBACK:
        try:
            district = city.lower()

            # Auto-train if not exists
            if not is_model_trained(district):
                train_model(district)

            # Use live pollutant data if partially available
            pm25 = data.get("pm25") if data else None
            pm10 = data.get("pm10") if data else None
            co = data.get("co") if data else 0
            no2 = data.get("no2") if data else 0
            so2 = data.get("so2") if data else 0
            o3 = data.get("o3") if data else 0

            # If no pollutant data available → use safe defaults
            if pm25 is None or pm10 is None:
                pm25, pm10 = 80, 120

            previous_aqi = data.get("aqi", 100) if data else 100

            features = [
                pm25,
                pm10,
                co or 0,
                no2 or 0,
                so2 or 0,
                o3 or 0,
                previous_aqi,
                previous_aqi - 5
            ]

            predicted_aqi = predict_current_aqi(district, features)

            if predicted_aqi is not None:

                short_term = forecast_short_term(district, features, 7)
                long_term = forecast_long_term(district, features, 30)

                return {
                    "pm25": float(pm25),
                    "pm10": float(pm10),
                    "co": float(co or 0),
                    "no2": float(no2 or 0),
                    "so2": float(so2 or 0),
                    "o3": float(o3 or 0),
                    "aqi": predicted_aqi,
                    "category": aqi_category(predicted_aqi),
                    "short_term_7_days": short_term,
                    "long_term_30_days": long_term,
                    "source": "District ML",
                    "data_type": "ml_predicted"
                }

        except Exception as e:
            print(f"[ML] Failed for {city}: {e}")

    # ❌ If absolutely everything fails
    return None
