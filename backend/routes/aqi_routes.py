from flask import Blueprint, request, jsonify
from services.aqi_service import get_realtime_aqi
from models.air_quality import AirQuality
from core import db

aqi_bp = Blueprint("aqi", __name__, url_prefix="/api/aqi")


@aqi_bp.route("/realtime", methods=["GET"])
def realtime_aqi():
    city = request.args.get("city", "").strip().lower()

    # Validate input
    if not city:
        return jsonify({
            "status": "error",
            "message": "city query parameter is required"
        }), 400

    # Hybrid AQI fetch
    data = get_realtime_aqi(city)

    if not data:
        return jsonify({
            "city": city,
            "status": "unavailable",
            "message": "No AQI data available for this location"
        }), 404

    # Save to DB
    record = AirQuality(
        city=city,
        pm25=data.get("pm25"),
        pm10=data.get("pm10"),
        co=data.get("co"),
        no2=data.get("no2"),
        so2=data.get("so2"),
        o3=data.get("o3"),
        category=data.get("category"),
        source=data.get("source"),
        data_type=data.get("data_type")
    )

    db.session.add(record)
    db.session.commit()

    # API Response
    return jsonify({
        "city": city,
        "pm25": record.pm25,
        "pm10": record.pm10,
        "co": record.co,
        "no2": record.no2,
        "so2": record.so2,
        "o3": record.o3,
        "category": record.category,
        "data_source": record.source,
        "data_type": record.data_type,
        "timestamp": record.timestamp.isoformat()
    }), 200
