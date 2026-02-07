from services.aqi_service import get_realtime_aqi
from services.weather_service import get_weather
from models.air_quality import AirQuality
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

    record = AirQuality(
        city=city,
        pm25=aqi_data["pm25"],
        pm10=aqi_data.get("pm10"),
        co=aqi_data.get("co"),
        no2=aqi_data.get("no2"),
        so2=aqi_data.get("so2"),
        o3=aqi_data.get("o3"),
        temperature=weather.get("temperature"),
        humidity=weather.get("humidity"),
        wind_speed=weather.get("wind_speed"),
        pressure=weather.get("pressure"),
        category=aqi_data["category"],
        source=aqi_data["source"],
        data_type=aqi_data["data_type"],
        timestamp=datetime.utcnow()
    )
    
   

    db.session.add(record)
    db.session.commit()
    
    
    return True
