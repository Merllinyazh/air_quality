from flask import Blueprint, jsonify, request
from models.air_quality import AirQuality
from services.advisory_service import medical_risk, seasonal_risk
from services.recovery_service import estimate_recovery
from services.school_service import school_advisory

advisory_bp = Blueprint("advisory", __name__, url_prefix="/api/advisory")


# -------------------------------------------------
# MEDICAL RISK (CITY-BASED)
# -------------------------------------------------
@advisory_bp.route("/medical", methods=["GET"])
def medical():
    city = request.args.get("city", "").lower().strip()

    if not city:
        return jsonify({"error": "city parameter required"}), 400

    record = (
        AirQuality.query
        .filter_by(city=city)
        .order_by(AirQuality.timestamp.desc())
        .first()
    )

    if not record or record.pm25 is None:
        return jsonify({
            "city": city,
            "status": "unavailable",
            "message": "No AQI data available"
        }), 404

    risk, advice, level = medical_risk(record.pm25)

    return jsonify({
        "city": city,
        "pm25": record.pm25,
        "risk_level": risk,
        "alert_level": level,
        "advice": advice
    })


# -------------------------------------------------
# MEDICAL RISK (DIRECT AQI – DASHBOARD FRIENDLY)
# -------------------------------------------------
@advisory_bp.route("/medical_risk", methods=["GET"])
def medical_direct():
    aqi = request.args.get("aqi", type=float)

    if aqi is None:
        return jsonify({"error": "aqi parameter required"}), 400

    risk, advice, level = medical_risk(aqi)

    return jsonify({
        "aqi": aqi,
        "risk_level": risk,
        "alert_level": level,
        "advice": advice
    })


# -------------------------------------------------
# RECOVERY TIME ESTIMATOR
# -------------------------------------------------
@advisory_bp.route("/recovery", methods=["GET"])
def recovery():
    aqi = request.args.get("aqi", type=float)
    wind = request.args.get("wind", default=5, type=float)

    if aqi is None:
        return jsonify({"error": "aqi parameter required"}), 400

    return jsonify({
        "aqi": aqi,
        "wind_speed": wind,
        "estimated_recovery_time": estimate_recovery(aqi, wind)
    })


# -------------------------------------------------
# SCHOOL OUTDOOR ADVISORY
# -------------------------------------------------
@advisory_bp.route("/school", methods=["GET"])
def school():
    aqi = request.args.get("aqi", type=float)

    if aqi is None:
        return jsonify({"error": "aqi parameter required"}), 400

    return jsonify({
        "aqi": aqi,
        "recommendation": school_advisory(aqi)
    })


# -------------------------------------------------
# SEASONAL POLLUTION RISK
# -------------------------------------------------
@advisory_bp.route("/seasonal", methods=["GET"])
def seasonal():
    return jsonify({
        "type": "Seasonal Pollution Risk",
        "data": seasonal_risk()
    })
