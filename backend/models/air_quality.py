from core import db
from datetime import datetime

class AirQuality(db.Model):
    __tablename__ = "air_quality"

    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(100), nullable=False)

    pm25 = db.Column(db.Float)
    pm10 = db.Column(db.Float)
    co = db.Column(db.Float)
    no2 = db.Column(db.Float)
    so2 = db.Column(db.Float)
    o3 = db.Column(db.Float)

    category = db.Column(db.String(50))
    source = db.Column(db.String(50))      # AQI.IN / OpenAQ / Nearest Station / ML
    data_type = db.Column(db.String(50))   # live / measured / estimated / predicted

    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
