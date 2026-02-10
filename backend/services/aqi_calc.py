# services/aqi_calculator.py

AQI_BREAKPOINTS = {
    "pm25": [
        (0, 30, 0, 50),
        (31, 60, 51, 100),
        (61, 90, 101, 200),
        (91, 120, 201, 300),
        (121, 250, 301, 400),
        (251, 500, 401, 500),
    ],
    "pm10": [
        (0, 50, 0, 50),
        (51, 100, 51, 100),
        (101, 250, 101, 200),
        (251, 350, 201, 300),
        (351, 430, 301, 400),
        (431, 600, 401, 500),
    ],
    "no2": [
        (0, 40, 0, 50),
        (41, 80, 51, 100),
        (81, 180, 101, 200),
        (181, 280, 201, 300),
        (281, 400, 301, 400),
        (401, 1000, 401, 500),
    ],
    "so2": [
        (0, 40, 0, 50),
        (41, 80, 51, 100),
        (81, 380, 101, 200),
        (381, 800, 201, 300),
        (801, 1600, 301, 400),
        (1601, 2000, 401, 500),
    ],
    "co": [
        (0, 1, 0, 50),
        (1.1, 2, 51, 100),
        (2.1, 10, 101, 200),
        (10.1, 17, 201, 300),
        (17.1, 34, 301, 400),
        (34.1, 50, 401, 500),
    ],
    "o3": [
        (0, 50, 0, 50),
        (51, 100, 51, 100),
        (101, 168, 101, 200),
        (169, 208, 201, 300),
        (209, 748, 301, 400),
        (749, 1000, 401, 500),
    ],
}


def calculate_sub_index(pollutant, concentration):
    if concentration is None:
        return None

    for bp_lo, bp_hi, i_lo, i_hi in AQI_BREAKPOINTS[pollutant]:
        if bp_lo <= concentration <= bp_hi:
            return round(
                ((i_hi - i_lo) / (bp_hi - bp_lo))
                * (concentration - bp_lo)
                + i_lo
            )
    return None


def get_aqi_category(aqi):
    if aqi <= 50:
        return "Good"
    elif aqi <= 100:
        return "Satisfactory"
    elif aqi <= 200:
        return "Moderate"
    elif aqi <= 300:
        return "Poor"
    elif aqi <= 400:
        return "Very Poor"
    return "Severe"


def calculate_aqi_from_pollutants(data):
    pollutants = {
        "pm25": data.get("pm25"),
        "pm10": data.get("pm10"),
        "no2": data.get("no2"),
        "so2": data.get("so2"),
        "co": data.get("co"),
        "o3": data.get("o3"),
    }

    sub_indices = {}

    for pollutant, value in pollutants.items():
        idx = calculate_sub_index(pollutant, value)
        if idx is not None:
            sub_indices[pollutant] = idx

    # CPCB minimum rule
    if len(sub_indices) < 3 or not any(
        p in sub_indices for p in ["pm25", "pm10"]
    ):
        return None

    final_aqi = max(sub_indices.values())
    dominant = max(sub_indices, key=sub_indices.get)

    return {
        "aqi": final_aqi,
        "category": get_aqi_category(final_aqi),
        "dominant_pollutant": dominant,
        "sub_indices": sub_indices,
    }
