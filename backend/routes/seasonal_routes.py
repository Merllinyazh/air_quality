from flask import Blueprint, jsonify
from core import db
from models.air_quality import AirQuality
from sqlalchemy import extract
import calendar

seasonal_bp = Blueprint("seasonal", __name__, url_prefix="/api/seasonal")


@seasonal_bp.route("/risk", methods=["GET"])
def seasonal_risk():
    results = (
        db.session.query(
            extract("month", AirQuality.timestamp).label("month"),
            db.func.avg(AirQuality.pm25).label("avg_pm25")
        )
        .group_by("month")
        .order_by("month")
        .all()
    )

    if not results:
        return jsonify({
            "status": "no_data",
            "message": "No historical AQI data available"
        }), 404

    seasonal_data = {}
    for month, avg in results:
        month_name = calendar.month_name[int(month)]
        seasonal_data[month_name] = round(avg, 2)

    return jsonify({
        "seasonal_pollution_risk": seasonal_data
    })
