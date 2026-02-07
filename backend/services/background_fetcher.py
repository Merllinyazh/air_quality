import time
from services.realtime_pipeline import fetch_and_store_realtime


# ALL Tamil Nadu districts / major cities
CITIES = [
    "chennai",
    "coimbatore",
    "madurai",
    "tiruchirappalli",
    "salem",
    "tirunelveli",
    "thoothukudi",
    "vellore",
    "erode",
    "dindigul",
    "thanjavur",
    "cuddalore",
    "nagapattinam",
    "karur",
    "namakkal",
    "krishnagiri",
    "dharmapuri",
    "kallakurichi",
    "ranipet",
    "tirupattur",
    "chengalpattu",
    "kanchipuram",
    "tiruvallur",
    "tiruvannamalai",
    "viluppuram",
    "perambalur",
    "ariyalur",
    "pudukkottai",
    "sivaganga",
    "ramanathapuram",
    "virudhunagar",
    "tenkasi",
    "the nilgiris",
    "kanyakumari",
    "mayiladuthurai"
]



def start_background_fetch(app):
  

    while True:
        with app.app_context():   # 🔥 THIS FIXES EVERYTHING
            for city in CITIES:
                try:
                    fetch_and_store_realtime(city)
                    print(f"[✓] Updated AQI & weather for {city}")
                except Exception as e:
                    print(f"[!] Failed for {city}: {e}")

        time.sleep(300)  # 5 minutes
