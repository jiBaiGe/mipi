'''
Created on May 16, 2019

@author: yez

'''
import os
import sys
from datetime import datetime

from flask import request, render_template, redirect, jsonify, send_file, url_for
from flask_login import current_user

from app.lib.milog import MiLog
from app.lib.project_root_path import root_path


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



    @app.route('/storage_page', methods=['GET'])
    def storage_page():
        return render_template("mainPage/storage_page.html")

    @app.route('/upload_file', methods=['POST'])
    def upload_file():
        try:
            MiLog.info("start upload file")
            now_time = datetime.now()
            file = request.files['file']
            username = current_user.username
            beyond_law = request.args.get('beyond_law')
            MiLog.info(username)
            file_name = file.filename
            MiLog.info("file name : %s" % file_name)

            if 'linux' in sys.platform:
                if beyond_law:
                    # os.mkdir(os.path.join("/home", "yez", "mipi", "data", username, "storage_file"))
                    file.save(os.path.join("/home", "yez", "mipi", "data", username, "storage_file", file_name))
                else:
                    file.save(os.path.join("/home", "yez", "mipi", "data", "storage_file", file_name))
            else:
                file.save(root_path()+"\\app\\static\\storage_file\\%s"%file_name)


            finish_time = datetime.now()
            spend_time = finish_time - now_time
            MiLog.info("finished in : %s seconds" % spend_time.seconds)
        except Exception as e:
            MiLog.exception(e)
            return jsonify({"upload": "failed"})


        return jsonify({"upload": "success"})

    @app.route('/storage/get_file', methods=['GET'])
    def get_file():
        username = current_user.username
        beyond_law = request.args.get('beyond_law')
        if 'linux' in sys.platform:

            sys_user_name = os.popen("whoami").read().replace("\n","")

            if beyond_law:
                mkdir = os.popen("mkdir -p /home/%s/mipi/data/%s/storage_file" % (sys_user_name, username)).read()
                save_dir = os.path.join("/home", sys_user_name, "mipi", "data", username,"storage_file")
                base_dir = "/storage/%s/download/"%username
            else:
                mkdir = os.popen("mkdir -p /home/%s/mipi/data/storage_file" % (sys_user_name)).read()
                save_dir = os.path.join("/home", sys_user_name,  "mipi", "data",  "storage_file")
                base_dir = "/storage/download/"
            dir_list = os.listdir(save_dir)
            return_json = list()
            for each_file in dir_list:
                if ".jpg" in each_file.lower() or ".png" in each_file.lower() or ".jpeg" in each_file.lower():
                    return_json.append({"name": each_file,
                                        "src": base_dir + each_file,
                                        "link": base_dir + each_file})
                else:
                    return_json.append({"name": each_file,
                                        "src": "static/images/file_icon.jpg",
                                        "link": base_dir + each_file})
        else:
            save_dir = os.path.join(root_path(), "app", "static", "storage_file")
            dir_list = os.listdir(save_dir)
            return_json = list()
            for each_file in dir_list:
                if ".jpg" in each_file.lower() or ".png" in each_file.lower() or ".jpeg" in each_file.lower():
                    return_json.append({"name": each_file,
                                        "src": "static/storage_file/" + each_file ,
                                        "link": "static/storage_file/" + each_file})
                else:
                    return_json.append({"name": each_file,
                                        "src": "static/images/file_icon.jpg",
                                        "link": "static/storage_file/" + each_file})


        return jsonify(return_json)

    @app.route('/storage/download/<file>', methods=['GET'])
    def download_file(file):

        file_path = os.path.join("/home", "yez",  "mipi", "data",  "storage_file", file)
        return send_file(file_path)

    @app.route('/storage/<username>/download/<file>', methods=['GET'])
    def download_beyond_file(username,file):

        file_path = os.path.join("/home", "yez", "mipi", "data", username, "storage_file", file)
        return send_file(file_path)

    @app.route('/user_profile', methods=['GET'])
    def user_profile_page():

        return render_template("mainPage/user_profile.html")

    @app.route('/beyond_law', methods=['GET'])
    def beyond_law():
        if hasattr(current_user, 'username'):
            return render_template("mainPage/beyond_law_page.html")
        else:
            return render_template("mainPage/login_page.html")

    @app.route('/private_upload', methods=['GET'])
    def private_upload():

        return render_template("mainPage/user_profile.html")

    return app
