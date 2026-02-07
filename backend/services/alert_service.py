def get_alert_level(category):
    """
    Returns alert level based on AQI category
    """

    alerts = {
        "Good": {
            "level": "Normal",
            "action": "No action required"
        },
        "Satisfactory": {
            "level": "Normal",
            "action": "Monitor air quality"
        },
        "Moderate": {
            "level": "Watch",
            "action": "Sensitive groups should be cautious"
        },
        "Poor": {
            "level": "Warning",
            "action": "Limit outdoor activities"
        },
        "Very Poor": {
            "level": "Critical",
            "action": "Avoid outdoor exposure"
        },
        "Severe": {
            "level": "Emergency",
            "action": "Health emergency. Stay indoors"
        }
    }

    return alerts.get(category, {
        "level": "Unknown",
        "action": "No alert available"
    })
