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

// Seasonal Risk
function getSeasonalRisk() {
    fetch(`${API_BASE}/api/seasonal/risk`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('seasonalResult').innerText = JSON.stringify(data, null, 2);
            updateSeasonalChart(data);
        })
        .catch(error => {
            document.getElementById('seasonalResult').innerText = `Error: ${error.message}`;
        });
}

// Initialize seasonal chart
let seasonalChart;
function initSeasonalChart() {
    const ctx = document.getElementById('seasonal-chart').getContext('2d');
    seasonalChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
            datasets: [{
                label: 'Seasonal AQI Risk',
                data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                borderColor: 'rgb(255, 99, 132)',
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                tension: 0.1
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

function updateSeasonalChart(data) {
    // Placeholder - update with actual seasonal data
    if (seasonalChart && data.seasonal_data) {
        seasonalChart.data.datasets[0].data = data.seasonal_data;
        seasonalChart.update();
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    initSeasonalChart();
});
