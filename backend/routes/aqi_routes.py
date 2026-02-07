from flask import Blueprint, request, jsonify
from services.aqi_service import get_realtime_aqi
from models.air_quality import AirQuality
from core import db

aqi_bp = Blueprint("aqi", __name__, url_prefix="/api/aqi")


@aqi_bp.route("/realtime")
def realtime_aqi():
    city = request.args.get("city", "").lower().strip()

    record = (
        AirQuality.query
        .filter_by(city=city)
        .order_by(AirQuality.timestamp.desc())
        .first()
    )

    if not record:
        return jsonify({
            "city": city,
            "status": "unavailable",
            "message": "No data yet. Wait for background update."
        }), 404

    return jsonify({
        "city": city,
        "pm25": record.pm25,
        "pm10": record.pm10,
        "co": record.co,
        "no2": record.no2,
        "so2": record.so2,
        "o3": record.o3,

        "temperature": record.temperature,
        "humidity": record.humidity,
        "wind_speed": record.wind_speed,
        "pressure": record.pressure,

        "category": record.category,
        "data_source": record.source,
        "data_type": record.data_type,
        "timestamp": record.timestamp.isoformat()
    })