from flask import Flask

from app.models import init_db
from app.routes import register_routes
from config import Config


def create_app():
    app = Flask(__name__, template_folder='templates')

    app.config.from_object(Config)

    init_db(app)

    register_routes(app)

    return app
