from flask import Flask

from config.database import init_app


def create_app(
) -> Flask:
    """
    Create Flask APP
    """
    app: Flask = Flask(__name__)

    # Init APP -> Database
    init_app(
        app=app
    )

    return app
