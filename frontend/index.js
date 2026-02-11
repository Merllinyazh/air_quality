const API_BASE = "http://127.0.0.1:5000";

async function loadDashboard(city) {
    try {
        const res = await fetch(`${API_BASE}/api/aqi/realtime?city=${city}`);
        const data = await res.json();

        if (data.status === "unavailable") {
            alert("No data available for " + city);
            return;
        }

        document.querySelector(".subtitle").innerText =
            `${city.toUpperCase()}, India`;

        document.getElementById("aqi").innerText = data.aqi ?? "—";
        document.getElementById("category").innerText = data.category ?? "—";

        document.getElementById("temp").innerText =
            data.temperature ? `${data.temperature}°C` : "—";

        document.getElementById("humidity").innerText =
            data.humidity ? `${data.humidity}%` : "—";

        document.getElementById("wind").innerText =
            data.wind_speed ? `${data.wind_speed} m/s` : "—";

        document.getElementById("pressure").innerText =
            data.pressure ? `${data.pressure} hPa` : "—";

        document.getElementById("updated").innerText =
            `Last updated: ${new Date(data.timestamp).toLocaleString()}`;

    } catch (err) {
        console.error("Dashboard error:", err);
    }
}

document.addEventListener("DOMContentLoaded", () => {
    const searchInput = document.getElementById("citySearch");

    loadDashboard("coimbatore");

    searchInput.addEventListener("change", () => {
        const city = searchInput.value.toLowerCase().trim();
        if (city) loadDashboard(city);
    });

    setInterval(() => {
        const city = searchInput.value || "coimbatore";
        loadDashboard(city.toLowerCase());
    }, 300000);
});
