from flask import Flask

from config.app import create_app

app: Flask = create_app()
