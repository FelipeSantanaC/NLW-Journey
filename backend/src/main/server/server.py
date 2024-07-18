from flask import Flask # type: ignore
from flask_cors import CORS # type: ignore
from src.main.routes.trips_routes import trips_routes_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(trips_routes_bp)