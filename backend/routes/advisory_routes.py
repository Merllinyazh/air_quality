from flask import Blueprint, jsonify, request
from services.advisory_service import get_health_advisory

advisory_bp = Blueprint("advisory", __name__, url_prefix="/api/advisory")


@advisory_bp.route("/", methods=["GET"])
def advisory():
    category = request.args.get("category")

    if not category:
        return jsonify({
            "status": "error",
            "message": "AQI category parameter is required"
        }), 400

    advisory = get_health_advisory(category)

    return jsonify({
        "category": category,
        "risk_level": advisory["risk"],
        "advisory_message": advisory["message"]
    })
