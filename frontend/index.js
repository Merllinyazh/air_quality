const API_BASE = "http://127.0.0.1:5000";

const DISTRICTS = [
    "coimbatore","chennai","madurai","tiruchirappalli","salem",
    "tirunelveli","vellore","erode","thoothukudi",
    "dindigul","thanjavur","cuddalore","namakkal","karur"
];

let districtChart;

// ---------- HELPERS ----------
const safe = (v, u="") => (v ?? v === 0) ? `${v}${u}` : "—";

// ---------- FEATURED CARD ----------
function renderFeatured(data, city) {
    return `
        <div class="featured-header">${city.toUpperCase()}</div>

        <div class="featured-aqi">
            <span class="pm">${Math.round(data.pm25)}</span>
            <span class="cat">${data.category}</span>
        </div>

        <div class="featured-weather">
            <div>🌡 Temperature <b>${safe(data.temperature,"°C")}</b></div>
            <div>💧 Humidity <b>${safe(data.humidity,"%")}</b></div>
            <div>🌬 Wind <b>${safe(data.wind_speed," m/s")}</b></div>
            <div>🧭 Pressure <b>${safe(data.pressure," hPa")}</b></div>
        </div>

        <div class="featured-footer">
            Source: ${data.data_source}<br/>
            ${new Date(data.timestamp).toLocaleString()}
        </div>
    `;
}

// ---------- MINI CARD ----------
function renderMiniCard(data, city) {
    return `
        <div class="city-card">
            <div class="city-name">${city.toUpperCase()}</div>
            <div class="aqi-value">${Math.round(data.pm25)}</div>
            <div class="category">${data.category}</div>
        </div>
    `;
}

// =====================================================
// 🏥 HEALTH & MEDICAL ADVISORY
// =====================================================
async function loadHealthAdvisory(aqi) {
    try {
        const res = await fetch(
            `${API_BASE}/api/advisory/medical_risk?aqi=${aqi}`
        );

        if (!res.ok) throw new Error("Medical API failed");

        const data = await res.json();

        // ✅ FIXED ID MAPPING
        document.getElementById("health-category").innerText =
            data.alert_level || "—";

        document.getElementById("medical-risk").innerText =
            data.risk_level || "—";

        document.getElementById("health-advice").innerText =
            data.advice || "—";

    } catch (err) {
        console.error("Medical advisory error:", err);

        document.getElementById("health-category").innerText = "—";
        document.getElementById("medical-risk").innerText = "—";
        document.getElementById("health-advice").innerText =
            "Unable to load advisory";
    }
}

// ---------- LOAD FEATURED CITY ----------
async function loadCity(city) {
    const res = await fetch(`${API_BASE}/api/aqi/realtime?city=${city}`);
    const data = await res.json();

    if (data.status === "unavailable") return;

    document.getElementById("featured-card").innerHTML =
        renderFeatured(data, city);

    // 🔥 Load medical advisory using PM2.5
    if (data.pm25 != null) {
        loadHealthAdvisory(data.pm25);
    }
}

// ---------- LOAD GRID ----------
async function loadGrid(exceptCity) {
    const grid = document.getElementById("cities-grid");
    grid.innerHTML = "";

    for (const city of DISTRICTS) {
        if (city === exceptCity) continue;

        try {
            const res = await fetch(`${API_BASE}/api/aqi/realtime?city=${city}`);
            const data = await res.json();

            if (data.status !== "unavailable" && data.pm25 != null) {
                grid.innerHTML += renderMiniCard(data, city);
            }
        } catch {
            console.warn("Grid skip:", city);
        }
    }
}

// ---------- DROPDOWN ----------
function initDropdown() {
    const select = document.getElementById("citySelect");

    DISTRICTS.forEach(city => {
        const opt = document.createElement("option");
        opt.value = city;
        opt.textContent = city.toUpperCase();
        select.appendChild(opt);
    });

    select.value = "coimbatore";

    select.addEventListener("change", () => {
        loadCity(select.value);
        loadGrid(select.value);
    });
}

// =====================================================
// 📊 DISTRICT-WISE AQI BAR CHART
// =====================================================
function initDistrictChart() {
    const ctx = document
        .getElementById("districtAqiChart")
        .getContext("2d");

    districtChart = new Chart(ctx, {
        type: "bar",
        data: {
            labels: [],
            datasets: [{
                label: "PM2.5 (µg/m³)",
                data: [],
                backgroundColor: "#007bff"
            }]
        },
        options: {
            responsive: true,
            plugins: { legend: { display: false } },
            scales: {
                y: {
                    beginAtZero: true,
                    title: { display: true, text: "PM2.5" }
                }
            }
        }
    });
}

async function loadDistrictAQIChart() {
    const labels = [];
    const values = [];

    for (const city of DISTRICTS) {
        try {
            const res = await fetch(
                `${API_BASE}/api/aqi/realtime?city=${city}`
            );
            const data = await res.json();

            if (data.status === "unavailable" || data.pm25 == null) continue;

            labels.push(city.toUpperCase());
            values.push(Math.round(data.pm25));

        } catch {
            console.warn("Chart skip:", city);
        }
    }

    districtChart.data.labels = labels;
    districtChart.data.datasets[0].data = values;
    districtChart.update();
}

// ---------- INIT ----------
document.addEventListener("DOMContentLoaded", () => {
    initDropdown();
    initDistrictChart();

    loadCity("coimbatore");        // DEFAULT FEATURED
    loadGrid("coimbatore");
    loadDistrictAQIChart();

    setInterval(() => {
        const selected = document.getElementById("citySelect").value;
        loadCity(selected);
        loadGrid(selected);
        loadDistrictAQIChart();
    }, 300000);
});
