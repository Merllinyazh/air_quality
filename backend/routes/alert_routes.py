from flask import Blueprint, jsonify, request
from services.alert_service import get_alert_level

alert_bp = Blueprint("alert", __name__, url_prefix="/api/alert")


@alert_bp.route("/", methods=["GET"])
def alert():
    category = request.args.get("category")

    if not category:
        return jsonify({
            "status": "error",
            "message": "AQI category parameter is required"
        }), 400

    alert_info = get_alert_level(category)

    return jsonify({
        "category": category,
        "alert_level": alert_info["level"],
        "recommended_action": alert_info["action"]
    })
