# # import pandas as pd
# # import joblib
# # import os
# # from sklearn.ensemble import RandomForestRegressor
# # from models.air_quality import AirQuality

# # MODEL_PATH = "models_store/aqi_model.pkl"

# # def train_model():
# #     records = AirQuality.query.all()
# #     df = pd.DataFrame([{
# #         "pm25": r.pm25,
# #         "pm10": r.pm10,
# #         "co": r.co,
# #         "no2": r.no2,
# #         "so2": r.so2,
# #         "o3": r.o3
# #     } for r in records])

# #     X = df
# #     y = df["pm25"]

# #     model = RandomForestRegressor(n_estimators=100)
# #     model.fit(X, y)

# #     os.makedirs("models_store", exist_ok=True)
# #     joblib.dump(model, MODEL_PATH)

# # def predict_aqi(data):
# #     model = joblib.load(MODEL_PATH)
# #     return model.predict([data])[0]

# # import numpy as np
# # from sklearn.ensemble import RandomForestRegressor

# # # Global model variable
# # _model = None


# # def is_model_trained():
# #     return _model is not None


# # def train_model():
# #     """
# #     Trains a simple ML model using dummy historical AQI-like data.
# #     In real deployment, this would be replaced with real historical data.
# #     """
# #     global _model

# #     # Example historical dataset (pm25, pm10, co, no2, so2, o3 → AQI)
# #     X = np.array([
# #         [60, 90, 0.8, 20, 8, 30],
# #         [80, 120, 1.2, 25, 10, 35],
# #         [110, 150, 1.5, 30, 12, 40],
# #         [150, 200, 2.0, 40, 15, 50],
# #         [200, 260, 2.5, 50, 20, 60]
# #     ])

# #     y = np.array([75, 95, 130, 180, 250])

# #     _model = RandomForestRegressor(
# #         n_estimators=100,
# #         random_state=42
# #     )
# #     _model.fit(X, y)


# # def predict_aqi(features):
# #     """
# #     Predict AQI using trained ML model
# #     """
# #     features = np.array(features).reshape(1, -1)
# #     return _model.predict(features)[0]
# import os
# import joblib
# import numpy as np
# from sklearn.ensemble import RandomForestRegressor

# MODEL_DIR = "models"
# MODEL_PATH = os.path.join(MODEL_DIR, "aqi_model.pkl")
# _model = None
# def is_model_trained():
#     return os.path.exists(MODEL_PATH)

# def train_model():
#     """
#     Train a simple AQI regression model (ONCE)
#     """
#     os.makedirs(MODEL_DIR, exist_ok=True)

#     # Dummy training data (exam-safe)
#     X = np.array([
#         [50, 80, 0.5, 20, 10, 30],
#         [80, 120, 1.0, 25, 15, 35],
#         [120, 160, 1.5, 30, 20, 40],
#         [200, 250, 2.5, 40, 30, 50],
#     ])

#     y = np.array([60, 95, 140, 220])  # AQI values

#     model = RandomForestRegressor(n_estimators=100, random_state=42)
#     model.fit(X, y)

#     joblib.dump(model, MODEL_PATH)
#     print("[✓] ML model trained and saved at:", MODEL_PATH)


# def load_model():
#     global _model
#     if _model is None:
#         if not os.path.exists(MODEL_PATH):
#             return None
#         _model = joblib.load(MODEL_PATH)
#         print("[✓] ML model loaded")
#     return _model


# def predict_aqi(features):
#     model = load_model()
#     if model is None:
#         return None

#     features = np.array(features).reshape(1, -1)
#     return float(model.predict(features)[0])

import os
import joblib
import numpy as np

from sklearn.ensemble import RandomForestRegressor, ExtraTreesRegressor
from sklearn.linear_model import LinearRegression, Lasso
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error

MODEL_DIR = "models"


# ---------------- DISTRICT PATHS ----------------

def _get_paths(district):
    district = district.lower().replace(" ", "_")

    model_path = os.path.join(MODEL_DIR, f"{district}_model.pkl")
    scaler_path = os.path.join(MODEL_DIR, f"{district}_scaler.pkl")
    name_path = os.path.join(MODEL_DIR, f"{district}_model_name.pkl")

    return model_path, scaler_path, name_path


# ---------------- CHECK ----------------

def is_model_trained(district):
    model_path, _, _ = _get_paths(district)
    return os.path.exists(model_path)


# ---------------- TRAIN ----------------

def train_model(district):

    os.makedirs(MODEL_DIR, exist_ok=True)

    district_seed = abs(hash(district)) % 1000
    np.random.seed(district_seed)

    X = np.array([
        [50, 80, 0.5, 20, 10, 30, 55, 50],
        [80, 120, 1.0, 25, 15, 35, 90, 85],
        [120, 160, 1.5, 30, 20, 40, 130, 120],
        [200, 250, 2.5, 40, 30, 50, 210, 200],
        [300, 350, 3.0, 50, 35, 60, 300, 280],
        [400, 450, 4.0, 60, 40, 70, 420, 390],
    ])

    X += np.random.normal(0, 5, X.shape)

    y = np.array([60, 95, 140, 220, 320, 450], dtype=float)
    y = y + np.random.normal(0, 10, y.shape)

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    models = {
        "RandomForest": RandomForestRegressor(n_estimators=200),
        "LinearRegression": LinearRegression(),
        "LassoRegression": Lasso(alpha=0.1),
        "ExtraTrees": ExtraTreesRegressor(n_estimators=200),
        "SVM": SVR()
    }

    results = {}

    for name, model in models.items():

        if name in ["LinearRegression", "LassoRegression", "SVM"]:
            model.fit(X_scaled, y)
            preds = model.predict(X_scaled)
        else:
            model.fit(X, y)
            preds = model.predict(X)

        rmse = np.sqrt(mean_squared_error(y, preds))
        results[name] = rmse

    best_model_name = min(results, key=results.get)
    best_model = models[best_model_name]

    if best_model_name in ["LinearRegression", "LassoRegression", "SVM"]:
        best_model.fit(X_scaled, y)
    else:
        best_model.fit(X, y)

    model_path, scaler_path, name_path = _get_paths(district)

    joblib.dump(best_model, model_path)
    joblib.dump(scaler, scaler_path)
    joblib.dump(best_model_name, name_path)

    print(f"[✓] Model trained for {district}")


# ---------------- LOAD ----------------

def load_model(district):

    model_path, scaler_path, name_path = _get_paths(district)

    if not os.path.exists(model_path):
        return None

    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    model_name = joblib.load(name_path)

    return model, scaler, model_name


# ---------------- PREDICT ----------------

def predict_current_aqi(district, features):

    model_data = load_model(district)
    if model_data is None:
        return None

    model, scaler, model_name = model_data

    features = np.array(features).reshape(1, -1)

    if model_name in ["LinearRegression", "LassoRegression", "SVM"]:
        features = scaler.transform(features)

    return round(float(model.predict(features)[0]), 2)


def forecast_short_term(district, features, days=7):

    forecasts = []
    current = features.copy()

    for _ in range(days):

        pred = predict_current_aqi(district, current)
        forecasts.append(pred)

        current[7] = current[6]
        current[6] = pred

    return forecasts


def forecast_long_term(district, features, days=30):
    return forecast_short_term(district, features, days)


def aqi_category(aqi):

    if aqi <= 50: return "Good"
    elif aqi <= 100: return "Satisfactory"
    elif aqi <= 200: return "Moderate"
    elif aqi <= 300: return "Poor"
    elif aqi <= 400: return "Very Poor"
    else: 
        return "Severe"

