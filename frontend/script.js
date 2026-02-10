const API_BASE = 'http://localhost:5000';

// Realtime AQI
function getRealtimeAQI() {
    const city = document.getElementById('cityInput').value.trim();
    if (!city) {
        alert('Please enter a city name');
        return;
    }

    fetch(`${API_BASE}/api/aqi/realtime?city=${encodeURIComponent(city)}`)
        .then(response => response.json())
        .then(data => {
            if (data.status === 'unavailable') {
                document.getElementById('aqiResult').innerText = `No data available for ${city}. ${data.message}`;
            } else {
                document.getElementById('aqiResult').innerText = JSON.stringify(data, null, 2);
            }
        })
        .catch(error => {
            document.getElementById('aqiResult').innerText = `Error: ${error.message}`;
        });
}

// Train ML Model
function trainModel() {
    fetch(`${API_BASE}/api/ml/train`, {
        method: 'POST'
    })
        .then(response => response.json())
        .then(data => {
            document.getElementById('trainResult').innerText = JSON.stringify(data, null, 2);
        })
        .catch(error => {
            document.getElementById('trainResult').innerText = `Error: ${error.message}`;
        });
}

// Predict AQI
document.getElementById('predictForm').addEventListener('submit', function(e) {
    e.preventDefault();

    const formData = new FormData(e.target);
    const data = {
        pm25: parseFloat(formData.get('pm25')),
        pm10: parseFloat(formData.get('pm10')),
        co: parseFloat(formData.get('co')),
        no2: parseFloat(formData.get('no2')),
        so2: parseFloat(formData.get('so2')),
        o3: parseFloat(formData.get('o3'))
    };

    fetch(`${API_BASE}/api/ml/predict`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
        .then(response => response.json())
        .then(data => {
            document.getElementById('predictResult').innerText = JSON.stringify(data, null, 2);
        })
        .catch(error => {
            document.getElementById('predictResult').innerText = `Error: ${error.message}`;
        });
});

// Seasonal Risk
function getSeasonalRisk() {
    fetch(`${API_BASE}/api/seasonal/risk`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('seasonalResult').innerText = JSON.stringify(data, null, 2);
        })
        .catch(error => {
            document.getElementById('seasonalResult').innerText = `Error: ${error.message}`;
        });
}
