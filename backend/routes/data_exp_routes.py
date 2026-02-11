from flask import Blueprint, request, jsonify
from models.air_quality import AirQuality
from sqlalchemy import func
from core import db

data_bp = Blueprint("data_explorer", __name__, url_prefix="/api/data-explorer")


@data_bp.route("/", methods=["GET"])
def get_data():
    search = request.args.get("search", "").lower()
    category = request.args.get("category", "")

    query = AirQuality.query

    if search:
        query = query.filter(AirQuality.city.ilike(f"%{search}%"))

    if category and category != "All":
        query = query.filter(AirQuality.category == category)

    records = query.all()

    data = []
    for r in records:
        data.append({
            "city": r.city,
            "aqi": r.aqi,
            "pm25": r.pm25,
            "pm10": r.pm10,
            "category": r.category,
            "timestamp": r.timestamp.isoformat()
        })

    return jsonify(data)
