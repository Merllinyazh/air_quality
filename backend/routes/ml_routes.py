# from flask import Blueprint, request, jsonify
# from services.ml_service import (
#     train_model,
#     predict_current_aqi,
#     forecast_future_aqi,
#     is_model_trained,
#     aqi_category,
#     load_model
# )

# ml_bp = Blueprint("ml", __name__, url_prefix="/api/ml")


# # ---------------- TRAIN ML MODEL ----------------
# @ml_bp.route("/train", methods=["POST"])
# def train():
#     train_model()
    
#     return jsonify({
#         "status": "success",
#         "message": "All ML models trained and best model selected successfully"
#     })


# # ---------------- PREDICT CURRENT AQI ----------------
# @ml_bp.route("/predict", methods=["POST"])
# def predict():

#     if not is_model_trained():
#         return jsonify({
#             "status": "error",
#             "message": "Model not trained yet. Train the model first."
#         }), 400

#     data = request.get_json()

#     required_fields = [
#         "pm25", "pm10", "co",
#         "no2", "so2", "o3",
#         "aqi_lag1", "aqi_lag2"
#     ]

#     missing = [f for f in required_fields if f not in data]

#     if missing:
#         return jsonify({
#             "status": "error",
#             "message": f"Missing fields: {', '.join(missing)}"
#         }), 400

#     features = [
#         data["pm25"],
#         data["pm10"],
#         data["co"],
#         data["no2"],
#         data["so2"],
#         data["o3"],
#         data["aqi_lag1"],
#         data["aqi_lag2"]
#     ]

#     current_prediction = predict_current_aqi(features)
#     future_prediction = forecast_future_aqi(features, days=5)
#     category = aqi_category(current_prediction)

#     # get selected model name
#     _, _, model_name = load_model()

#     return jsonify({
#         "status": "success",
#         "current_aqi": current_prediction,
#         "category": category,
#         "future_5_days": future_prediction,
#         "model_used": model_name
#     })
from flask import Blueprint, request, jsonify
from services.ml_service import (
    predict_current_aqi,
    forecast_short_term,
    forecast_long_term,
    is_model_trained,
    train_model,
    aqi_category
)
from utils.dist_coords import DISTRICT_COORDS
from services.aqi_service import get_realtime_aqi

ml_bp = Blueprint("ml", __name__, url_prefix="/api/ml")


# ---------------- TRAIN DISTRICT MODEL ----------------
@ml_bp.route("/train", methods=["POST"])
def train():

    data = request.get_json()
    district = data.get("district", "").lower()

    if district not in DISTRICT_COORDS:
        return jsonify({"error": "Invalid district"}), 400

    train_model(district)

    return jsonify({
        "status": "success",
        "message": f"Model trained successfully for {district}"
    })


# ---------------- DISTRICT PREDICTION ----------------
@ml_bp.route("/district-predict", methods=["POST"])
def district_predict():

    data = request.get_json()
    district = data.get("district", "").lower()

    if district not in DISTRICT_COORDS:
        return jsonify({"error": "Invalid district"}), 400

    # Auto-train if not trained
    if not is_model_trained(district):
        train_model(district)

    required_fields = ["pm25", "pm10", "co", "no2", "so2", "o3"]

    missing = [f for f in required_fields if f not in data]

    if missing:
        return jsonify({
            "error": f"Missing fields: {', '.join(missing)}"
        }), 400

    features = [
        data["pm25"],
        data["pm10"],
        data["co"],
        data["no2"],
        data["so2"],
        data["o3"],
        data.get("aqi_lag1", 100),
        data.get("aqi_lag2", 95)
    ]

    current = predict_current_aqi(district, features)
    short_term = forecast_short_term(district, features, 7)
    long_term = forecast_long_term(district, features, 30)

    return jsonify({
        "district": district,
        "current_aqi": current,
        "category": aqi_category(current),
        "short_term_7_days": short_term,
        "long_term_30_days": long_term
    })

@ml_bp.route("/auto-predict", methods=["POST"])
def auto_predict():

    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "No JSON body received"}), 400

    district = data.get("district", "").lower()

    if not district:
        return jsonify({"error": "District required"}), 400

    # ------------------------------------------------
    # 1️⃣ GET LIVE DATA (Same as Dashboard)
    # ------------------------------------------------
    live_data = get_realtime_aqi(district)

    if not live_data:
        return jsonify({"error": "Unable to fetch live AQI"}), 500

    pm25 = live_data.get("pm25", 80)
    pm10 = live_data.get("pm10", 120)
    co = live_data.get("co", 0)
    no2 = live_data.get("no2", 0)
    so2 = live_data.get("so2", 0)
    o3 = live_data.get("o3", 0)

    official_aqi = live_data.get("aqi", 100)

    # ------------------------------------------------
    # 2️⃣ PREPARE FEATURES FOR ML
    # ------------------------------------------------
    features = [
        pm25,
        pm10,
        co,
        no2,
        so2,
        o3,
        official_aqi,        # lag1
        official_aqi - 5     # lag2
    ]

    # ------------------------------------------------
    # 3️⃣ TRAIN MODEL IF NOT EXISTS
    # ------------------------------------------------
    if not is_model_trained(district):
        train_model(district)

    # ------------------------------------------------
    # 4️⃣ FORECAST USING ML (ONLY FUTURE)
    # ------------------------------------------------
    short_term = forecast_short_term(district, features, 7)
    long_term = forecast_long_term(district, features, 30)

    # ------------------------------------------------
    # 5️⃣ RETURN OFFICIAL CURRENT + ML FORECAST
    # ------------------------------------------------
    return jsonify({
        "district": district,
        "aqi": official_aqi,  # ✅ SAME AS DASHBOARD
        "category": aqi_category(official_aqi),
        "source": live_data.get("source", "Live Data"),
        "short_term_7_days": short_term,
        "long_term_30_days": long_term
    })

    
