from flask import Blueprint, render_template, request, redirect, url_for, session
from . import db
from sqlalchemy import text

main = Blueprint('main', __name__)

@main.route('/')
def login():
    return render_template('login.html')

@main.route('/login', methods=['POST'])
def login_post():
    username = request.form['username']
    password = request.form['password']
    result = db.session.execute(text("SELECT * FROM users WHERE username = :u AND password = :p"),
                                {'u': username, 'p': password})
    user = result.fetchone()
    if user:
        session['user'] = username
        return redirect(url_for('main.home'))
    return "Invalid credentials", 401

@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db.session.execute(text("INSERT INTO users (username, password) VALUES (:u, :p)"),
                           {'u': username, 'p': password})
        db.session.commit()
        return redirect(url_for('main.login'))
    return render_template('register.html')

@main.route('/home')
def home():
    if 'user' not in session:
        return redirect(url_for('main.login'))
    return render_template('home.html', username=session['user'])

@main.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('main.login'))
