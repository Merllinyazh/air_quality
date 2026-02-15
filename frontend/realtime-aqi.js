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

// Initialize map



let heatLayer;

/* ---------------- DARK MODE ---------------- */
document.getElementById("dark-mode-toggle").onclick = () => {
    document.body.classList.toggle("dark-mode");
    document.getElementById("dark-mode-toggle").textContent =
        document.body.classList.contains("dark-mode") ? "☀️" : "🌙";
};

/* ---------------- MAP INIT ---------------- */
let map;
let districtLayer;

/* ---------------- MAP INIT (TAMIL NADU LOCKED) ---------------- */
function initMap() {
    const tamilNaduBounds = [
        [8.0, 76.5],   // SW
        [13.6, 80.5]   // NE
    ];

    map = L.map("map", {
        center: [11.1271, 78.6569],
        zoom: 7,
        minZoom: 7,
        maxZoom: 10,
        maxBounds: tamilNaduBounds,
        maxBoundsViscosity: 1.0
    });

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution: "© OpenStreetMap contributors",
        noWrap: true
    }).addTo(map);

    addLegend();
    loadDistrictBorders();
}

/* ---------------- AQI COLOR SCALE ---------------- */
function getAQIColor(pm25) {
    return pm25 <= 50 ? "#00e400" :
           pm25 <= 100 ? "#ffff00" :
           pm25 <= 150 ? "#ff7e00" :
           pm25 <= 200 ? "#ff0000" :
           pm25 <= 300 ? "#8f3f97" :
                         "#7e0023";
}

function getAQIStatus(pm25) {
    if (pm25 <= 50) return "Good";
    if (pm25 <= 100) return "Moderate";
    if (pm25 <= 150) return "Unhealthy (Sensitive)";
    if (pm25 <= 200) return "Unhealthy";
    if (pm25 <= 300) return "Very Unhealthy";
    return "Hazardous";
}

/* ---------------- LOAD DISTRICT BORDERS (RAW FIXED) ---------------- */
async function loadDistrictBorders() {
    const res = await fetch(
        "https://raw.githubusercontent.com/datameet/maps/master/Districts/tamil-nadu.geojson"
    );
    const geoData = await res.json();

    districtLayer = L.geoJSON(geoData, {
        style: {
            color: "#1f2933",
            weight: 1.2,
            fillOpacity: 0.6
        },
        onEachFeature: onEachDistrict
    }).addTo(map);

   
}

/* ---------------- DISTRICT STYLE + POPUP ---------------- */
function onEachDistrict(feature, layer) {
    const district = feature.properties.district;
    const pm25 = Math.floor(Math.random() * 250) + 20;

    layer.setStyle({
        fillColor: getAQIColor(pm25)
    });

    layer.bindPopup(`
        <b>${district}</b><br>
        PM2.5: ${pm25}<br>
        Status: ${getAQIStatus(pm25)}
    `);
}

/* ---------------- TIME-BASED AQI ANIMATION ---------------- */




/* ---------------- LEGEND ---------------- */
function addLegend() {
    const legend = L.control({ position: "bottomright" });

    legend.onAdd = () => {
        const div = L.DomUtil.create("div", "legend");
        div.innerHTML = `
            <b>AQI Levels</b><br>
            <i style="background:#00e400"></i> Good<br>
            <i style="background:#ffff00"></i> Moderate<br>
            <i style="background:#ff7e00"></i> Unhealthy (S)<br>
            <i style="background:#ff0000"></i> Unhealthy<br>
            <i style="background:#8f3f97"></i> Very Unhealthy<br>
            <i style="background:#7e0023"></i> Hazardous
        `;
        return div;
    };

    legend.addTo(map);
}

/* ---------------- LOAD ---------------- */
document.addEventListener("DOMContentLoaded", initMap);

