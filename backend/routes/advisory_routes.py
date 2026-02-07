from flask import Blueprint, jsonify, request
from models.air_quality import AirQuality
from services.advisory_service import medical_risk, seasonal_risk
from services.recovery_service import estimate_recovery
from services.school_service import school_advisory

advisory_bp = Blueprint("advisory", __name__, url_prefix="/api/advisory")

@advisory_bp.route("/medical")
def medical():
    city = request.args.get("city", "").lower()
    record = AirQuality.query.filter_by(city=city)\
        .order_by(AirQuality.timestamp.desc()).first()

    risk, advice = medical_risk(record.pm25)

    return jsonify({
        "city": city,
        "risk_level": risk,
        "advice": advice
    })


@advisory_bp.route("/recovery")
def recovery():
    aqi = float(request.args.get("aqi"))
    wind = float(request.args.get("wind", 5))

    return jsonify({
        "estimated_recovery_time": estimate_recovery(aqi, wind)
    })


@advisory_bp.route("/school")
def school():
    aqi = float(request.args.get("aqi"))
    return jsonify({
        "recommendation": school_advisory(aqi)
    })


@advisory_bp.route("/seasonal")
def seasonal():
    return jsonify(seasonal_risk())
