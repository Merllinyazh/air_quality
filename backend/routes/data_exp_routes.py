from flask import Blueprint, jsonify
from models.air_quality import AirQuality
from sqlalchemy import func
from core import db

data_bp = Blueprint("data_explorer", __name__, url_prefix="/api/data-explorer")


@data_bp.route("/stats", methods=["GET"])
def get_overall_stats():

    # 🔹 Total unique locations
    total_locations = db.session.query(
        func.count(func.distinct(AirQuality.city))
    ).scalar()

    # 🔹 Overall average AQI
    avg_aqi = db.session.query(
        func.avg(AirQuality.aqi)
    ).scalar()

    # 🔹 Highest AQI record
    highest_record = (
        AirQuality.query
        .order_by(AirQuality.aqi.desc())
        .first()
    )

    # 🔹 Lowest AQI record
    lowest_record = AirQuality.query \
    .filter(AirQuality.aqi.isnot(None)) \
    .order_by(AirQuality.aqi.asc()) \
    .first()

    # 🔹 Average AQI for EACH city
    city_averages = (
        db.session.query(
            AirQuality.city,
            func.avg(AirQuality.aqi).label("avg_aqi")
        )
        .group_by(AirQuality.city)
        .all()
    )

    city_avg_list = [
        {
            "city": city,
            "avg_aqi": round(avg, 2)
        }
        for city, avg in city_averages
    ]

    return jsonify({
        "total_locations": total_locations or 0,
        "avg_aqi": round(avg_aqi, 2) if avg_aqi else 0,
        "highest": {
            "city": highest_record.city if highest_record else None,
            "aqi": highest_record.aqi if highest_record else 0
        },
        "lowest": {
            "city": lowest_record.city if lowest_record else None,
            "aqi": lowest_record.aqi if lowest_record else 0
        },
        "city_average_aqi": city_avg_list
    })
    
    # ===============================================
# DISTRICT ANALYTICS (ADD BELOW /stats)
# ===============================================

@data_bp.route("/district/<city>", methods=["GET"])
def get_district_stats(city):

    city = city.lower()

    records = (
        AirQuality.query
        .filter(func.lower(AirQuality.city) == city)
        .order_by(AirQuality.timestamp.asc())
        .all()
    )

    if not records:
        return jsonify({
            "message": "No data found for this district"
        }), 404

    # Extract AQI values safely
    aqis = [r.aqi for r in records if r.aqi is not None]

    if not aqis:
        return jsonify({
            "message": "No AQI values available"
        }), 404

    avg_aqi = round(sum(aqis) / len(aqis), 2)
    highest_aqi = max(aqis)
    lowest_aqi = min(aqis)

    return jsonify({
        "city": city,
        "total_locations": 1,
        "avg_aqi": avg_aqi,
        "highest_aqi": highest_aqi,
        "lowest_aqi": lowest_aqi,
        "records": [
            {
                "city": r.city,
                "aqi": r.aqi,
                "pm25": r.pm25,
                "pm10": r.pm10,
                "category": r.category,
                "timestamp": r.timestamp.isoformat()
            }
            for r in records
        ]
    })

@data_bp.route("/district/<city>/monthly-trend", methods=["GET"])
def get_monthly_trend(city):

    city = city.lower()

    # Group by YEAR + MONTH
    monthly_data = (
        db.session.query(
            func.extract("year", AirQuality.timestamp).label("year"),
            func.extract("month", AirQuality.timestamp).label("month"),
            func.avg(AirQuality.aqi).label("avg_aqi")
        )
        .filter(
            func.lower(AirQuality.city) == city,
            AirQuality.aqi.isnot(None)
        )
        .group_by("year", "month")
        .order_by("year", "month")
        .all()
    )

    if not monthly_data:
        return jsonify({
            "message": "No monthly trend data found"
        }), 404

    return jsonify([
        {
            "year": int(year),
            "month": int(month),
            "avg_aqi": round(avg_aqi, 2)
        }
        for year, month, avg_aqi in monthly_data
    ])
