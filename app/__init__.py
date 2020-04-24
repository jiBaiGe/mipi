from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app import config
from app.db import db

app = Flask(__name__)

app.config.from_pyfile('config.py')
from app.main_page_api import main_page_api
app = main_page_api(app)

from app.user_control import user_control
app = user_control(app)

with app.app_context():
    db.init_app(app)
    db.create_all()  # create uncreated tables
    db.app = app

if __name__ == "__main__":
    app.run()
