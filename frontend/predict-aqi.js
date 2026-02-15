const API_BASE = 'http://localhost:5000';

// ---------------- DARK MODE ----------------
document.getElementById('dark-mode-toggle').addEventListener('click', function () {
    document.body.classList.toggle('dark-mode');
    const isDark = document.body.classList.contains('dark-mode');
    this.textContent = isDark ? '☀️' : '🌙';
    localStorage.setItem('darkMode', isDark);
});

if (localStorage.getItem('darkMode') === 'true') {
    document.body.classList.add('dark-mode');
    document.getElementById('dark-mode-toggle').textContent = '☀️';
}


// ---------------- PREDICT AQI ----------------
document.getElementById('predictForm').addEventListener('submit', function (e) {

    e.preventDefault();

    const formData = new FormData(e.target);
    const district = formData.get('district');

    document.getElementById('predictResult').innerText =
        "Fetching live data & running ML prediction...";

    fetch(`${API_BASE}/api/ml/auto-predict`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ district: district })
    })
        .then(response => response.json())
        .then(data => {

            if (data.error) {
                document.getElementById('predictResult').innerText = data.error;
                return;
            }

            document.getElementById('predictResult').innerHTML = `
                <h3>Current AQI: ${data.aqi}</h3>
                <p><strong>Category:</strong> ${data.category}</p>
                <p><strong>Source:</strong> ${data.source}</p>
            `;

            updateCharts(data);
        })
        .catch(error => {
            document.getElementById('predictResult').innerText =
                `Error: ${error.message}`;
        });
});


// ---------------- CHARTS ----------------
let shortTermChart;
let longTermChart;

function initCharts() {

    const shortCanvas = document.getElementById('short-term-chart');
    const longCanvas = document.getElementById('long-term-chart');

    if (!shortCanvas || !longCanvas) {
        console.warn("Chart canvas not found.");
        return;
    }

    shortTermChart = new Chart(shortCanvas.getContext('2d'), {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Short-Term AQI',
                data: [],
                borderWidth: 2,
                tension: 0.3,
                fill: false
            }]
        },
        options: {
            responsive: true,
            scales: { y: { beginAtZero: true } }
        }
    });

    longTermChart = new Chart(longCanvas.getContext('2d'), {
        type: 'bar',   // bar looks better for long term
        data: {
            labels: [],
            datasets: [{
                label: 'Long-Term AQI',
                data: [],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: { y: { beginAtZero: true } }
        }
    });
}


function updateCharts(data) {

    if (!shortTermChart || !longTermChart) return;

    // -------- SHORT TERM --------
    const shortLabels = ["Today"];
    const shortValues = [data.aqi];

    if (data.short_term_7_days) {
        data.short_term_7_days.forEach((_, i) => {
            shortLabels.push(`Day ${i + 1}`);
        });

        shortValues.push(...data.short_term_7_days);
    }

    shortTermChart.data.labels = shortLabels;
    shortTermChart.data.datasets[0].data = shortValues;
    shortTermChart.update();


    // -------- LONG TERM --------
    const longLabels = [];
    const longValues = [];

    if (data.long_term_30_days) {
        data.long_term_30_days.forEach((val, i) => {
            longLabels.push(`Day ${i + 1}`);
            longValues.push(val);
        });
    }

    longTermChart.data.labels = longLabels;
    longTermChart.data.datasets[0].data = longValues;
    longTermChart.update();
}


// ---------------- INIT ----------------
document.addEventListener('DOMContentLoaded', function () {
    initCharts();
});
