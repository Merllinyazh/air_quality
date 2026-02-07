def school_advisory(aqi):
    if aqi <= 50:
        return "Safe for all outdoor activities"
    elif aqi <= 100:
        return "Limited outdoor activity"
    else:
        return "Indoor-only activities recommended"
