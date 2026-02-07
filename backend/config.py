import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///air_quality.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    AQI_API_KEY = os.getenv("AQI_API_KEY")
    ENABLE_ML_FALLBACK = True
