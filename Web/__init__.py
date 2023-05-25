from flask import Flask
from .views import views
from dotenv import load_dotenv
import os

load_dotenv()

def create_app():
    app = Flask(__name__)
    key = "kunle_manel-flask234ffrdf"
    app.config['SECRET_KEY'] = key
    app.register_blueprint(views,url_prefix='/')
    return app