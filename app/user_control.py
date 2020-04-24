'''
Created on Nov 1, 2018

@author: Zhaoyu

'''
import datetime

from flask import abort, request, jsonify, render_template,redirect,url_for,flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from wtforms import StringField, BooleanField, PasswordField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm

from app import db
from app.models import User
from functools import wraps


class LoginForm(FlaskForm):
    username = StringField('User Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('remember me', default=True)


def login_required_json_return(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        if current_user.is_authenticated:
            return func(*args, **kwargs)
        else:
            return jsonify({"error": "need_login"})
    return wrapped


# def record_vistor(ip_address,username,action):
#     access_time = datetime.datetime.now().strftime('%Y-%m-%d')
#     if AccessRecord.query.filter_by(username=username, ip_address=ip_address, date=access_time, action=action).all() == []:
#         record = AccessRecord(username=username, ip_address=ip_address, action=action, date=access_time, action_times=1)
#         db.session.add(record)
#
#     else:
#         one_user_today = AccessRecord.query.filter_by(username=username, ip_address=ip_address, date=access_time, action=action).first()
#         AccessRecord.query.filter_by(username=username, ip_address=ip_address, date=access_time, action=action).first().action_times = one_user_today.action_times+1
#     db.session.commit()


def user_control(app):
    login_manager = LoginManager()
    login_manager.session_protection = 'strong'
    login_manager.login_view = 'login_event'
    login_manager.init_app(app=app)


    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        user_name = request.form.get('username')
        password = request.form.get('password')
        remember_me = request.form.get('remember_me')

        # if form.validate_on_submit():
        user = User.query.filter_by(username=user_name).first()
        if user is None:
            flash('Login failed! User not exists.')

            return redirect(url_for('login_page'))
        if check_password_hash(user.hash_password, password):
            login_user(user, remember=True)
            return redirect(url_for('main_page'))
        else:
            flash('Log in failed. wrong password', 'danger')
            return redirect(url_for('login_page'))


    @app.route('/logout', methods=['GET', 'POST'])
    @login_required
    def logout():
        logout_user()
        return jsonify({"logout":"true"})

    # @app.route('/login_event')
    # def login_event():
    #     return redirect(url_for('lcc', event="document.getElementById('login').style.display='block'") )

    @app.route('/create_user', methods=['GET', 'POST'])
    def create_user():
        name = request.form.get('username')
        password = request.form.get('password')
        password_twice = request.form.get('password_twice')
        if password == password_twice:
            user = User.query.filter_by(username=name).first()
            if user is None:
                hash_password = generate_password_hash(password)
                record = User(username=name, level=1, info="", hash_password=hash_password)
                db.session.add(record)
                db.session.commit()
                flash("user has been added to database")
                return redirect(url_for('login_page'))
            else:
                flash("user exists, please login")
                return redirect(url_for('login_page'))
        else:
            flash("New Password was different with New Password Again")
            return render_template("mainPage/register_page.html")

    @app.route('/register', methods=['GET'])
    def register():
        return render_template("mainPage/register_page.html")

    @app.route('/get_user', methods=['GET'])
    def get_user():
        now_user = current_user.username if hasattr(current_user, 'username') else "Login"
        print(current_user)
        return jsonify({"username":now_user})

    return app