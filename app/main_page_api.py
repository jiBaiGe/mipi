'''
Created on May 16, 2019

@author: Zhaoyu

'''
from flask import request, render_template

from app.lib.milog import MiLog


def main_page_api(app):

    @app.before_request
    def before():
        visitor_ip = request.remote_addr
        MiLog.info("new visitor: %s" %visitor_ip)

    @app.route('/', methods=['GET'])
    def warroom():
        return '<h1>Mipi, start!</h1>'

    @app.route('/main_page', methods=['GET'])
    def main_page():
        return render_template("mainPage/main_page.html")

    return app
