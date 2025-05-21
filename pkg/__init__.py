from flask import Flask
from flask_wtf import CSRFProtect
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

from pkg import config # the class is the BaseConfig

# Load environment variables from .env file (if present)
load_dotenv()

csrf = CSRFProtect()

def create_app():
    from pkg.models import db
    app = Flask(__name__, instance_relative_config=True) # load config from instance folder
    app.config['SECRET_KEY'] = '59InUNHh4Yqh2yzW_ieqv5CBOJnmW0Z73E2hZhPT8Ss'

    app.config.from_pyfile("config.py")
    app.config.from_object(config.TestConfig) # load config from the class

    # Protect our routes with csrf
    csrf.init_app(app)

    db.init_app(app)
    migrate = Migrate(app, db)

    return app

app = create_app()

from pkg import staticroutes