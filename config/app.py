from environs import Env
from flask import Flask
from flask_jwt_extended import JWTManager


def create_app(
) -> Flask:
    """
    Create Flask APP
    """
    from config.logger import logger
    from config.database import init_db
    from backend.user.apis import user_bp

    # Read ENV File
    env = Env()
    env.read_env('.env')

    try:
        app: Flask = Flask(__name__)

        # Configure JWT
        app.config["JWT_SECRET_KEY"] = env("JWT_SECRET_KEY")
        JWTManager(app)

        """
        Register APIs
        """
        app.register_blueprint(user_bp)

    except Exception as e:
        logger.error(f"An Unexpected Error occurred while create Flask App | {e}")
    else:
        try:
            # Init DB
            init_db(
                app=app
            )

            """
            Register Models
            """
            from backend.user.models import User

        except Exception as e:
            logger.error(f"An Unexpected Error occurred while Init Database | {e}")
        else:
            return app
