from flask import Flask

from app import config


app = Flask(__name__)

app.config.from_pyfile('config.py')

from app.main_page_api import main_page_api
app = main_page_api(app)

if __name__ == "__main__":
    app.run()
