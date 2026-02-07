from flask import Blueprint, request, jsonify
from services.alert_service import alert_level

alert_bp = Blueprint("alerts", __name__, url_prefix="/api/alerts")

# Early warning & alert level
@alert_bp.route("/", methods=["GET"])
def alerts():
    pm25 = float(request.args.get("pm25"))
    return jsonify({
        "alert_level": alert_level(pm25)
    })
