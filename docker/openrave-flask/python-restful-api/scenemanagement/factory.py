from flask import Flask
from werkzeug.utils import find_modules, import_string
from pymongo import MongoClient


def create_app(config=None):
    app = Flask(__name__)

    app.config.update(dict(
        DATABASE='openrave',
    ))
    app.config.update(config or {})

    app.client = MongoClient('mongodb://localhost:27017/')
    app.db = app.client[app.config['DATABASE']]
    app.collection = app.db['scenes']

    register_blueprints(app)

    return app


def register_blueprints(app):
    """Register all blueprint modules
    Reference: Armin Ronacher, "Flask for Fun and for Profit" PyBay 2016.
    """
    for name in find_modules('scenemanagement.scene'):
        mod = import_string(name)
        if hasattr(mod, 'bp'):
            app.register_blueprint(mod.bp)
    return None
