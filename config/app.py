from flask import Flask


def create_app(
) -> Flask:
    """
    Create Flask APP
    """
    from config.logger import logger
    from config.database import init_db

    try:
        app: Flask = Flask(__name__)
    except Exception as e:
        logger.error(f"An Unexpected Error occurred while create Flask App | {e}")
    else:
        try:
            # Init DB
            init_db(
                app=app
            )
        except Exception as e:
            logger.error(f"An Unexpected Error occurred while Init Database | {e}")

        return app
