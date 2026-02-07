from core import db
from datetime import datetime

class Alert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(50))
    aqi = db.Column(db.Float)
    level = db.Column(db.String(20))
    message = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
