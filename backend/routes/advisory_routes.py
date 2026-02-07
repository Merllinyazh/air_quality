from flask import Blueprint, request, jsonify
from services.advisory_service import medical_risk, school_advice

advisory_bp = Blueprint("advisory", __name__, url_prefix="/api/advisory")

# Medical risk (simulation-based)
@advisory_bp.route("/medical", methods=["GET"])
def medical():
    pm25 = float(request.args.get("pm25"))
    return jsonify({
        "risk": medical_risk(pm25),
        "note": "Simulation-based advisory only"
    })

# School outdoor activity advisor
@advisory_bp.route("/school", methods=["GET"])
def school():
    pm25 = float(request.args.get("pm25"))
    return jsonify({
        "recommendation": school_advice(pm25)
    })

