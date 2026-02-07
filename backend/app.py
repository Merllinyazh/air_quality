from flask import Flask
from flask_cors import CORS
from config import Config
from core import db, CORS

from routes.aqi_routes import aqi_bp
from routes.ml_routes import ml_bp
from routes.alert_routes import alert_bp
from routes.advisory_routes import advisory_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)

    db.init_app(app)

    app.register_blueprint(aqi_bp)
    app.register_blueprint(ml_bp)
    app.register_blueprint(alert_bp)
    app.register_blueprint(advisory_bp)

    return app

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
