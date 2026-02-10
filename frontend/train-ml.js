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

// Train ML Model
function trainModel() {
    document.getElementById('trainResult').innerText = 'Training model... Please wait.';
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
