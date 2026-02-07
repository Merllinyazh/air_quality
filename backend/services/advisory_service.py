from core import db
from models.air_quality import AirQuality
from sqlalchemy import extract, func

def seasonal_risk():
    data = db.session.query(
        extract("month", AirQuality.timestamp).label("month"),
        func.avg(AirQuality.pm25).label("avg_pm25")
    ).group_by("month").all()

    result = {}
    for month, avg in data:
        risk = "Low"
        if avg > 200:
            risk = "High"
        elif avg > 100:
            risk = "Medium"

        result[int(month)] = {
            "avg_pm25": round(avg, 2),
            "risk": risk
        }

    return result
def medical_risk(aqi):
    if aqi <= 100:
        return ("Low", "Normal precautions")
    elif aqi <= 200:
        return ("Medium", "Doctor consultation recommended")
    else:
        return ("High", "Immediate medical attention advised")
