from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from ..extensions import db  # Import your database instance from your main app module
from ..database.models import User  # Import your User model


# Creating the Blueprint
auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('auth.login'))  # Note the Blueprint name prefix
    return render_template('register.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    user_id = session.get('user_id')
    if user_id:
        return redirect(url_for('main_chat'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for('main_chat'))  # Assuming 'main' is the Blueprint name for your main app routes
        else:
            flash('Invalid username or password.')
    return render_template('login.html')

@auth.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))  # Assuming 'main.index' is the route to your main page
