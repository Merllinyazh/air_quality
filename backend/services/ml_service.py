# import pandas as pd
# import joblib
# import os
# from sklearn.ensemble import RandomForestRegressor
# from models.air_quality import AirQuality

# MODEL_PATH = "models_store/aqi_model.pkl"

# def train_model():
#     records = AirQuality.query.all()
#     df = pd.DataFrame([{
#         "pm25": r.pm25,
#         "pm10": r.pm10,
#         "co": r.co,
#         "no2": r.no2,
#         "so2": r.so2,
#         "o3": r.o3
#     } for r in records])

#     X = df
#     y = df["pm25"]

#     model = RandomForestRegressor(n_estimators=100)
#     model.fit(X, y)

#     os.makedirs("models_store", exist_ok=True)
#     joblib.dump(model, MODEL_PATH)

# def predict_aqi(data):
#     model = joblib.load(MODEL_PATH)
#     return model.predict([data])[0]

import numpy as np
from sklearn.ensemble import RandomForestRegressor

# Global model variable
_model = None


def is_model_trained():
    return _model is not None


def train_model():
    """
    Trains a simple ML model using dummy historical AQI-like data.
    In real deployment, this would be replaced with real historical data.
    """
    global _model

    # Example historical dataset (pm25, pm10, co, no2, so2, o3 → AQI)
    X = np.array([
        [60, 90, 0.8, 20, 8, 30],
        [80, 120, 1.2, 25, 10, 35],
        [110, 150, 1.5, 30, 12, 40],
        [150, 200, 2.0, 40, 15, 50],
        [200, 260, 2.5, 50, 20, 60]
    ])

    y = np.array([75, 95, 130, 180, 250])

    _model = RandomForestRegressor(
        n_estimators=100,
        random_state=42
    )
    _model.fit(X, y)


def predict_aqi(features):
    """
    Predict AQI using trained ML model
    """
    features = np.array(features).reshape(1, -1)
    return _model.predict(features)[0]
