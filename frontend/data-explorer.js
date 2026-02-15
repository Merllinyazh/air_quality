const API_BASE = "http://localhost:5000";

let chart;
let globalData = [];
let chartType = "bar"; 




/* =====================================
   PART 2 — OVERALL DASHBOARD CARDS
===================================== */

async function loadOverallStats() {

    try {
        const res = await fetch(
            `${API_BASE}/api/data-explorer/stats`
        );

        const stats = await res.json();

        document.getElementById("totalLocations").innerText =
            stats.total_locations;

        document.getElementById("avgAQI").innerText =
            stats.avg_aqi;

        document.getElementById("maxAQI").innerText =
            `${stats.highest.aqi} (${stats.highest.city})`;

        document.getElementById("minAQI").innerText =
            `${stats.lowest.aqi} (${stats.lowest.city})`;

        // Optional: Render city average chart
        renderCityAverageChart(stats.city_average_aqi);

    } catch (err) {
        console.error("Error loading stats:", err);
    }
}


/* =====================================
   CITY AVERAGE CHART (FROM BACKEND)
===================================== */

function renderCityAverageChart(cityData) {

    if (!cityData || !cityData.length) return;

    const ctx = document.getElementById("aqiChart").getContext("2d");

    if (chart) chart.destroy();

    chart = new Chart(ctx, {
        type: "bar",
        data: {
            labels: cityData.map(c => c.city),
            datasets: [{
                label: "Average AQI",
                data: cityData.map(c => c.avg_aqi),
                backgroundColor: "#1f4e79"
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });
}





/* =====================================
   CHART FOR FILTERED SEARCH DATA
===================================== */

// default

function toggleChartType() {
    chartType = chartType === "bar" ? "line" : "bar";
    renderChart(globalData);
}

/* AQI Category Color */
function getAQIColor(category) {
    switch (category) {
        case "Good": return "#00e400";
        case "Satisfactory": return "#9cff00";
        case "Moderate": return "#ffff00";
        case "Poor": return "#ff7e00";
        case "Very Poor": return "#ff0000";
        case "Severe": return "#7e0023";
        default: return "#999999";
    }
}

function toggleChartType() {
    chartType = chartType === "bar" ? "line" : "bar";

    document.getElementById("chartToggleBtn").innerText =
        chartType === "bar"
            ? "Switch to Line Chart"
            : "Switch to Bar Chart";

    renderChart(globalData);
}
function renderChart(data) {

    if (!data.length) return;

    const ctx = document.getElementById("aqiChart").getContext("2d");

    if (chart) chart.destroy();

    // Filter valid AQI values
    const filtered = data.filter(d => d.aqi !== null);

    // Gradient animation
    const gradient = ctx.createLinearGradient(0, 0, 0, 400);
    gradient.addColorStop(0, "#1f4e79");
    gradient.addColorStop(1, "#4fa3d1");

    chart = new Chart(ctx, {
        type: chartType,
        data: {
            labels: filtered.map(d => d.city),
            datasets: [
                {
                    label: "AQI",
                    data: filtered.map(d => d.aqi),

                    backgroundColor:
                        chartType === "bar"
                            ? filtered.map(d => getAQIColor(d.category))
                            : gradient,

                    borderColor: "#1f4e79",
                    borderWidth: 2,
                    tension: 0.4, // smooth line
                    fill: chartType === "line"
                },

                // 🔴 AQI Threshold Line (Poor = 200)
                {
                    label: "Threshold (200)",
                    data: Array(filtered.length).fill(200),
                    borderColor: "red",
                    borderWidth: 2,
                    borderDash: [5, 5],
                    type: "line",
                    fill: false,
                    pointRadius: 0
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                mode: "index",
                intersect: false
            },
            plugins: {
                tooltip: {
                    callbacks: {
                        afterBody: function(context) {

                            const index = context[0].dataIndex;
                            const cityData = filtered[index];

                            return [
                                `PM2.5: ${cityData.pm25}`,
                                `PM10: ${cityData.pm10}`,
                                `Category: ${cityData.category}`
                            ];
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 500
                }
            }
        }
    });
}

/* =========================================================
   DISTRICT SEARCH OVERRIDE (ADD THIS BELOW YOUR CODE)
========================================================= */

async function searchDistrict() {

    const district = document.getElementById("citySearch").value;

    if (!district) {
        alert("Enter district name");
        return;
    }

    currentDistrict = district.toLowerCase();

    try {
        const res = await fetch(
            `${API_BASE}/api/data-explorer/district/${district}`
        );

        if (!res.ok) {
            alert("District not found");
            return;
        }

        const data = await res.json();

        if (!data.records || !Array.isArray(data.records)) {
            alert("Invalid data format");
            return;
        }

        // 🔹 Update cards using backend values
        document.getElementById("totalLocations").innerText =
            data.total_locations;

        document.getElementById("avgAQI").innerText =
            data.avg_aqi;

        document.getElementById("maxAQI").innerText =
            data.highest_aqi;

        document.getElementById("minAQI").innerText =
            data.lowest_aqi;

        
        renderSingleDistrictChart(district, data.avg_aqi);

    } catch (err) {
        console.error("District search error:", err);
    }
}



function renderSingleDistrictChart(city, avgAQI) {

    const ctx = document.getElementById("aqiChart").getContext("2d");

    if (chart) chart.destroy();

    chart = new Chart(ctx, {
        type: "bar",
        data: {
            labels: [city],   // 🔥 Only one label
            datasets: [{
                label: "Average AQI",
                data: [avgAQI],   // 🔥 Only one value
                backgroundColor: "#1f4e79",
                barThickness: 60,          // fixed width
                maxBarThickness: 70,
                categoryPercentage: 0.5,
                barPercentage: 0.5
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 500
                }
            }
        }
    });
}

function updateDistrictCards(records) {

    const aqis = records
        .map(r => r.aqi)
        .filter(a => a !== null);

    if (!aqis.length) return;

    const avg = Math.round(
        aqis.reduce((a,b)=>a+b,0) / aqis.length
    );

    const max = Math.max(...aqis);
    const min = Math.min(...aqis);

    document.getElementById("totalLocations").innerText = 1;
    document.getElementById("avgAQI").innerText = avg;
    document.getElementById("maxAQI").innerText = max;
    document.getElementById("minAQI").innerText = min;
}

async function showMonthlyTrend() {

    if (!currentDistrict) {
        alert("Search district first");
        return;
    }

    try {
        const res = await fetch(
            `${API_BASE}/api/data-explorer/district/${currentDistrict}/monthly-trend`
        );

        if (!res.ok) {
            alert("No monthly trend data");
            return;
        }

        const trendData = await res.json();

        if (!trendData.length) {
            alert("No monthly data available");
            return;
        }

        const ctx = document.getElementById("aqiChart").getContext("2d");

        if (chart) chart.destroy();

        chart = new Chart(ctx, {
            type: "line",
            data: {
                labels: trendData.map(d => `${d.month}/${d.year}`),
                datasets: [{
                    label: `${currentDistrict} Monthly AQI`,
                    data: trendData.map(d => d.avg_aqi),
                    backgroundColor: "#1f4e79",
                    borderRadius: 6,
                    barThickness: 35
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 500
                    }
                }
            }
        });

    } catch (err) {
        console.error("Monthly trend error:", err);
    }
}



/* =====================================
   INIT
===================================== */

document.addEventListener("DOMContentLoaded", () => {
    loadOverallStats();      // Cards + City Avg Chart
    
});
