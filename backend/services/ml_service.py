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

# import numpy as np
# from sklearn.ensemble import RandomForestRegressor

# # Global model variable
# _model = None


# def is_model_trained():
#     return _model is not None


# def train_model():
#     """
#     Trains a simple ML model using dummy historical AQI-like data.
#     In real deployment, this would be replaced with real historical data.
#     """
#     global _model

#     # Example historical dataset (pm25, pm10, co, no2, so2, o3 → AQI)
#     X = np.array([
#         [60, 90, 0.8, 20, 8, 30],
#         [80, 120, 1.2, 25, 10, 35],
#         [110, 150, 1.5, 30, 12, 40],
#         [150, 200, 2.0, 40, 15, 50],
#         [200, 260, 2.5, 50, 20, 60]
#     ])

#     y = np.array([75, 95, 130, 180, 250])

#     _model = RandomForestRegressor(
#         n_estimators=100,
#         random_state=42
#     )
#     _model.fit(X, y)


# def predict_aqi(features):
#     """
#     Predict AQI using trained ML model
#     """
#     features = np.array(features).reshape(1, -1)
#     return _model.predict(features)[0]
import os
import joblib
import numpy as np
from sklearn.ensemble import RandomForestRegressor

MODEL_DIR = "models"
MODEL_PATH = os.path.join(MODEL_DIR, "aqi_model.pkl")
_model = None
def is_model_trained():
    return os.path.exists(MODEL_PATH)

def train_model():
    """
    Train a simple AQI regression model (ONCE)
    """
    os.makedirs(MODEL_DIR, exist_ok=True)

    # Dummy training data (exam-safe)
    X = np.array([
        [50, 80, 0.5, 20, 10, 30],
        [80, 120, 1.0, 25, 15, 35],
        [120, 160, 1.5, 30, 20, 40],
        [200, 250, 2.5, 40, 30, 50],
    ])

    y = np.array([60, 95, 140, 220])  # AQI values

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)

    joblib.dump(model, MODEL_PATH)
    print("[✓] ML model trained and saved at:", MODEL_PATH)


def load_model():
    global _model
    if _model is None:
        if not os.path.exists(MODEL_PATH):
            return None
        _model = joblib.load(MODEL_PATH)
        print("[✓] ML model loaded")
    return _model


def predict_aqi(features):
    model = load_model()
    if model is None:
        return None

    features = np.array(features).reshape(1, -1)
    return float(model.predict(features)[0])
