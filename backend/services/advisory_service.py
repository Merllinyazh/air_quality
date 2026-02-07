def medical_risk(pm25):
    if pm25 < 100: return "Low"
    elif pm25 < 200: return "Medium"
    return "High"

def school_advice(pm25):
    if pm25 < 100: return "Safe"
    elif pm25 < 150: return "Limited"
    return "Indoor Only"
