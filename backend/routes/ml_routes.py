from flask import Blueprint, request, jsonify
from services.ml_service import train_model, predict_aqi, is_model_trained

ml_bp = Blueprint("ml", __name__, url_prefix="/api/ml")


# ---------------- TRAIN ML MODEL ----------------
@ml_bp.route("/train", methods=["POST"])
def train():
    train_model()
    return jsonify({
        "status": "success",
        "message": "ML model trained successfully"
    })


# ---------------- PREDICT AQI ----------------
@ml_bp.route("/predict", methods=["POST"])
def predict():
    if not is_model_trained():
        return jsonify({
            "status": "error",
            "message": "Model not trained yet. Train the model first."
        }), 400

    data = request.get_json()

    required_fields = ["pm25", "pm10", "co", "no2", "so2", "o3"]
    missing = [f for f in required_fields if f not in data]

    if missing:
        return jsonify({
            "status": "error",
            "message": f"Missing fields: {', '.join(missing)}"
        }), 400

    features = [
        data["pm25"],
        data["pm10"],
        data["co"],
        data["no2"],
        data["so2"],
        data["o3"]
    ]

    prediction = predict_aqi(features)

    return jsonify({
        "status": "success",
        "predicted_aqi": round(float(prediction), 2),
        "data_type": "predicted",
        "model": "RandomForestRegressor"
    })
