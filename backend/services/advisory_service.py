def get_health_advisory(category):
    """
    Returns health advisory message based on AQI category
    """

    advisories = {
        "Good": {
            "risk": "Low",
            "message": "Air quality is satisfactory. Safe for outdoor activities."
        },
        "Satisfactory": {
            "risk": "Low",
            "message": "Air quality is acceptable. Sensitive individuals should take minor precautions."
        },
        "Moderate": {
            "risk": "Medium",
            "message": "People with respiratory issues should limit prolonged outdoor exertion."
        },
        "Poor": {
            "risk": "High",
            "message": "Avoid outdoor activities. Sensitive groups should stay indoors."
        },
        "Very Poor": {
            "risk": "High",
            "message": "Serious health risk. Outdoor activities should be avoided."
        },
        "Severe": {
            "risk": "Critical",
            "message": "Health emergency conditions. Everyone should remain indoors."
        }
    }

    return advisories.get(category, {
        "risk": "Unknown",
        "message": "No advisory available"
    })
