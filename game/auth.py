from flask import Blueprint, render_template, flash, redirect, url_for, request
from .model import User
from werkzeug.security import generate_password_hash, check_password_hash
from game import db
from flask_login import login_user, logout_user, current_user


auth = Blueprint('auth', __name__)


@auth.route("/register", methods=['GET', 'POST'])
def register_page():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email_address=email).first()
        name = User.query.filter_by(username=username).first()
        if user:
            flash('Email already exist', category='danger')
        elif name:
            flash('Username already exist')
        elif len(email) < 4:
            flash('Email must be greater than four characters', category='danger')
        elif len(username) < 2:
            flash('username must be greater the 1 characters', category='danger')
        elif password1 != password2:
            flash('Password don\'t match.', category='danger')
        elif len(password1) < 6:
            flash('password must be at least 6 characters.', category='danger')
        else:
            user_to_create = User(username=username,
                              email_address=email,
                              password=generate_password_hash(password1, method='sha256'))
            db.session.add(user_to_create)
            db.session.commit()
            login_user(user_to_create)
            flash(f'account was created successfully', category='success')
            return redirect(url_for('views.game_page'))
    return render_template('register.html', user=current_user)


@auth.route("/login", methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.game_page'))
            else:
                flash('Incorrect password, try again.', category='danger')
        else:
            flash('username does not exist', category='danger')

    return render_template('login.html', user=current_user)


@auth.route("/logout")
def logout_page():
    logout_user()
    flash('You have been logged out', category='success')
    return redirect(url_for('views.home_page'))
