from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
from core import db
from config import Config

# Routes
from routes.aqi_routes import aqi_bp
from routes.ml_routes import ml_bp
from routes.seasonal_routes import seasonal_bp
from routes.alert_routes import alert_bp
from routes.advisory_routes import advisory_bp
from routes.data_exp_routes import data_bp

# Background job
from services.background_fetcher import start_background_fetch

import threading


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)
    db.init_app(app)

    app.register_blueprint(aqi_bp)
    app.register_blueprint(ml_bp)
    app.register_blueprint(seasonal_bp)
    app.register_blueprint(alert_bp)
    app.register_blueprint(advisory_bp) 
    app.register_blueprint(data_bp)

    @app.errorhandler(404)
    def not_found(error):
        if request.path.startswith('/api'):
            return jsonify({"error": "Not Found", "message": "The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again."}), 404
        else:
            return send_from_directory('../frontend', 'index.html'), 404

    # Serve frontend static files
    @app.route('/')
    def serve_index():
        return send_from_directory('../frontend', 'index.html')

    @app.route('/<path:filename>')
    def serve_static(filename):
        return send_from_directory('../frontend', filename)

    return app


app = create_app()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print("[✓] Database initialized")

    # ✅ PASS APP TO THREAD
    bg_thread = threading.Thread(
        target=start_background_fetch,
        args=(app,),        # 🔥 THIS FIXES CONTEXT
        daemon=True
    )
    bg_thread.start()

    print("[✓] Background AQI fetcher started (every 5 minutes)")
    print("[✓] Data sources: OpenAQ + Open-Meteo")
    print("[✓] ML fallback enabled")

    app.run(debug=True, host="0.0.0.0", port=5000)
