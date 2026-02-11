const API_BASE = "http://localhost:5000";
let chart;
let globalData = [];

async function loadData() {
    const search = document.getElementById("searchInput").value;
    const category = document.getElementById("categoryFilter").value;

    const res = await fetch(
        `${API_BASE}/api/data-explorer/?search=${search}&category=${category}`
    );

    const data = await res.json();
    globalData = data;

    renderOverview(data);
    renderTable(data);
    renderChart(data);
}

function renderOverview(data) {
    if (data.length === 0) return;

    const aqis = data.map(d => d.aqi).filter(a => a != null);

    document.getElementById("totalLocations").innerText = data.length;
    document.getElementById("avgAQI").innerText =
        Math.round(aqis.reduce((a,b)=>a+b,0)/aqis.length);
    document.getElementById("maxAQI").innerText = Math.max(...aqis);
    document.getElementById("minAQI").innerText = Math.min(...aqis);
}

function renderTable(data) {
    const tbody = document.querySelector("#dataTable tbody");
    tbody.innerHTML = "";

    data.forEach(d => {
        tbody.innerHTML += `
            <tr>
                <td>${d.city}</td>
                <td>${d.aqi}</td>
                <td>${d.pm25}</td>
                <td>${d.pm10}</td>
                <td>${d.category}</td>
            </tr>
        `;
    });
}

function renderChart(data) {
    const ctx = document.getElementById("aqiChart").getContext("2d");

    if (chart) chart.destroy();

    chart = new Chart(ctx, {
        type: "bar",
        data: {
            labels: data.map(d => d.city),
            datasets: [{
                label: "AQI",
                data: data.map(d => d.aqi),
                backgroundColor: "#007bff"
            }]
        }
    });
}

function downloadCSV() {
    let csv = "City,AQI,PM2.5,PM10,Category\n";

    globalData.forEach(d => {
        csv += `${d.city},${d.aqi},${d.pm25},${d.pm10},${d.category}\n`;
    });

    const blob = new Blob([csv], { type: "text/csv" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = "aqi_data.csv";
    link.click();
}

document.addEventListener("DOMContentLoaded", loadData);
