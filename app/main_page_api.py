'''
Created on May 16, 2019

@author: Zhaoyu

'''
from flask import request, render_template, redirect

from app.lib.milog import MiLog


def main_page_api(app):

    @app.before_request
    def before():
        visitor_ip = request.remote_addr
        MiLog.info("new visitor: %s" %visitor_ip)

    @app.route('/', methods=['GET'])
    def hello_mipi():
        return redirect('/main_page')

    @app.route('/main_page', methods=['GET'])
    def main_page():
        return render_template("mainPage/main_page.html")

    @app.route('/login_page', methods=['GET'])
    def login_page():
        return render_template("mainPage/login_page.html")

    @app.route('/register_page', methods=['GET'])
    def register_page():
        return render_template("mainPage/register_page.html")

    return app
