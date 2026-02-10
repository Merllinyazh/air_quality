const API_BASE = 'http://localhost:5000';

// Dark mode toggle
document.getElementById('dark-mode-toggle').addEventListener('click', function() {
    document.body.classList.toggle('dark-mode');
    const isDark = document.body.classList.contains('dark-mode');
    this.textContent = isDark ? '☀️' : '🌙';
    localStorage.setItem('darkMode', isDark);
});

// Load dark mode preference
if (localStorage.getItem('darkMode') === 'true') {
    document.body.classList.add('dark-mode');
    document.getElementById('dark-mode-toggle').textContent = '☀️';
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
            updatePredictionChart(data);
        })
        .catch(error => {
            document.getElementById('predictResult').innerText = `Error: ${error.message}`;
        });
});

// Initialize prediction chart
let predictionChart;
function initPredictionChart() {
    const ctx = document.getElementById('prediction-chart').getContext('2d');
    predictionChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Predicted AQI'],
            datasets: [{
                label: 'AQI Value',
                data: [0],
                backgroundColor: 'rgba(75, 192, 192, 0.6)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

function updatePredictionChart(data) {
    if (predictionChart && data.predicted_aqi !== undefined) {
        predictionChart.data.datasets[0].data = [data.predicted_aqi];
        predictionChart.update();
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    initPredictionChart();
});
