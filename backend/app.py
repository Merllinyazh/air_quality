from flask import Flask
from config import Config
from core import db, cors

# Import blueprints
from routes.aqi_routes import aqi_bp
from routes.advisory_routes import advisory_bp
from routes.alert_routes import alert_bp
from routes.ml_routes import ml_bp
from routes.seasonal_routes import seasonal_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    cors.init_app(app)

    # Register routes
    app.register_blueprint(aqi_bp)
    app.register_blueprint(advisory_bp)
    app.register_blueprint(alert_bp)
    app.register_blueprint(ml_bp)
    app.register_blueprint(seasonal_bp)

    # Create database tables
    with app.app_context():
        db.create_all()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
