from environs import Env
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# Read ENV File
env = Env()
env.read_env('.env')

db: SQLAlchemy = SQLAlchemy()
migrate: Migrate = Migrate()


def init_db(
        app: Flask
) -> None:
    """
    Config Flask with PostgreSQL and Init APP
    """
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{env("POSTGRES_USER")}:{env("POSTGRES_PASSWORD")}@postgres:5432/default_name'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)
