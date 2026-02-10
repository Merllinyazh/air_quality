from services.aqi_service import get_realtime_aqi
from services.weather_service import get_weather
from models.air_quality import AirQuality
from services.aqi_calc import calculate_aqi_from_pollutants
from core import db
from datetime import datetime


def fetch_and_store_realtime(city):
    """
    SINGLE SOURCE OF TRUTH:
    AQI + Weather → DB
    """

    aqi_data = get_realtime_aqi(city)
    if not aqi_data:
        return False

    weather = get_weather(city)

        # 3️⃣ Debug check (TEMP – you can remove later)
    print("[DEBUG] AQI DATA:", aqi_data)
    print("[DEBUG] WEATHER DATA:", weather)

    # 4️⃣ Create DB record safely
    record = AirQuality(
        city=city,

        # Pollutants
        pm25=aqi_data.get("pm25"),
        pm10=aqi_data.get("pm10"),
        co=aqi_data.get("co"),
        no2=aqi_data.get("no2"),
        so2=aqi_data.get("so2"),
        o3=aqi_data.get("o3"),

        # AQI fields (IMPORTANT)
        aqi=aqi_data.get("aqi"),
        dominant_pollutant=aqi_data.get("dominant_pollutant"),
        category=aqi_data.get("category"),

        # Weather
        temperature=weather.get("temperature"),
        humidity=weather.get("humidity"),
        wind_speed=weather.get("wind_speed"),
        pressure=weather.get("pressure"),

        # Metadata
        source=aqi_data.get("source"),
        data_type=aqi_data.get("data_type"),
        timestamp=datetime.utcnow()
    )

    # 5️⃣ Store in DB
    try:
        db.session.add(record)
        db.session.commit()
        print(f"[SUCCESS] Stored AQI for {city}")
        return True
    except Exception as e:
        db.session.rollback()
        print(f"[DB ERROR] Failed to store AQI for {city}: {e}")
        return False