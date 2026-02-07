def get_alert_level(category):
    """
    Returns alert level and advisory message based on AQI category
    """

    alerts = {
        "Good": {
            "level": "Normal",
            "action": "Air quality is good. Enjoy outdoor activities."
        },
        "Satisfactory": {
            "level": "Normal",
            "action": "Air quality is acceptable. Sensitive individuals should monitor symptoms."
        },
        "Moderate": {
            "level": "Watch",
            "action": "People with respiratory issues should limit prolonged outdoor exertion."
        },
        "Poor": {
            "level": "Warning",
            "action": "Avoid outdoor activities. Sensitive groups should stay indoors."
        },
        "Very Poor": {
            "level": "Critical",
            "action": "Health risk for everyone. Stay indoors and avoid physical exertion."
        },
        "Severe": {
            "level": "Emergency",
            "action": "Severe health risk. Remain indoors and seek medical help if needed."
        }
    }

    # Fallback (safety)
    return alerts.get(category, {
        "level": "Unknown",
        "action": "Air quality data unavailable. Please monitor updates."
    })
