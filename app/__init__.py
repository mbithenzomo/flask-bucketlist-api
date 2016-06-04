from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(configuration):
    app = Flask(__name__)
    app.config.from_object(configuration)

    db.init_app(app)

    return app
