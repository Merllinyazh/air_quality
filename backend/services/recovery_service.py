def estimate_recovery(aqi, wind_speed=5):
    if aqi <= 100:
        return "0 – 6 hours"
    elif aqi <= 200:
        return f"{int(24 / wind_speed)} hours"
    else:
        return f"{int(72 / wind_speed)} hours"
