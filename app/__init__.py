from flask import Flask, render_template
from config import Config
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
# from flask_mail import Mail, Message
# from flask_login import LoginManager

App = Flask(__name__)
App.config.from_object(Config)

# db = SQLAlchemy(app)
# migrate = Migrate(app, db)

# mail = Mail(app)

# login = LoginManager(app)
# login.login_view = 'login'
# login.login_message = 'danger'

from app import routes, models