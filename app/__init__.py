from flask import Flask

from . import config


app = Flask(__name__)

app.config.from_pyfile('config.py')

from main_page_api import main_page_api
app = main_page_api(app)