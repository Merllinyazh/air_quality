def alert_level(pm25):
    if pm25 > 300: return "Critical"
    elif pm25 > 200: return "Warning"
    elif pm25 > 100: return "Watch"
    return "Normal"
