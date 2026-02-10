from flask import Blueprint, jsonify, request
from services.alert_service import get_alert_level
from flask import Blueprint, jsonify, request
from models.air_quality import AirQuality
from models.alert import Alert
from core import db

alert_bp = Blueprint("alerts", __name__, url_prefix="/api/alerts")

@alert_bp.route("/check", methods=["GET"])
def check_alert():
    city = request.args.get("city", "").lower()

    record = AirQuality.query.filter_by(city=city)\
        .order_by(AirQuality.timestamp.desc()).first()

    if not record:
        return jsonify({"error": "No AQI data found"}), 404

    alert_data = get_alert_level(record.category)

    alert = Alert(
        city=city,
        aqi=record.pm25,
        level=alert_data["level"],
        message=alert_data["action"]
    )
    db.session.add(alert)
    db.session.commit()

    return jsonify({
        "city": city,
        "aqi": record.pm25,
        "alert_level": alert_data["level"],
        "message": alert_data["action"],
        "timestamp": alert.timestamp.isoformat()
    })
