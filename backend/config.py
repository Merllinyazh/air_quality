import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Database
    SQLALCHEMY_DATABASE_URI = "sqlite:///air_quality.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # AQI API (WAQI / AQI.IN)
    AQI_API_KEY = os.getenv("AQI_API_KEY")

    # ML fallback switch
    ENABLE_ML_FALLBACK = True
