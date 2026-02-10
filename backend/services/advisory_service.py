from core import db
from models.air_quality import AirQuality
from sqlalchemy import extract, func


# ---------------------------------------------
# MEDICAL RISK LOGIC
# ---------------------------------------------
def medical_risk(aqi):
    """
    Returns:
    - risk_level: Low / Medium / High
    - advice: human readable message
    - alert_level: Watch / Warning / Critical
    """

    if aqi <= 50:
        return (
            "Low",
            "Air quality is good. No health impact expected.",
            "Normal"
        )

    elif aqi <= 100:
        return (
            "Low",
            "Sensitive individuals should monitor symptoms.",
            "Watch"
        )

    elif aqi <= 200:
        return (
            "Medium",
            "Doctor consultation recommended for respiratory issues.",
            "Warning"
        )

    else:
        return (
            "High",
            "Immediate medical attention advised. Avoid outdoor exposure.",
            "Critical"
        )

# ---------------------------------------------
# SEASONAL RISK ANALYSIS (MONTH-WISE)
# ---------------------------------------------
def seasonal_risk():
    data = (
        db.session.query(
            extract("month", AirQuality.timestamp).label("month"),
            func.avg(AirQuality.pm25).label("avg_pm25")
        )
        .filter(AirQuality.pm25.isnot(None))
        .group_by("month")
        .order_by("month")
        .all()
    )

    result = {}

    for month, avg in data:
        if avg > 200:
            risk = "High"
        elif avg > 100:
            risk = "Medium"
        else:
            risk = "Low"

        result[int(month)] = {
            "average_pm25": round(avg, 2),
            "risk_level": risk
        }

    return result
