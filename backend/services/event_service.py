def event_advice(predicted_aqi):
    if predicted_aqi <= 100:
        return "Proceed with event"
    elif predicted_aqi <= 200:
        return "Consider rescheduling"
    else:
        return "Move event indoors"
