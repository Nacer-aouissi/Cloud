# app/routes.py
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from .db import get_db_connection

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return redirect(url_for('main.login'))

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user:
            session['user'] = username
            return redirect(url_for('main.home'))
        else:
            flash('Invalid credentials')
    return render_template('login.html')

@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        conn.commit()
        cur.close()
        conn.close()

        return redirect(url_for('main.login'))
    return render_template('register.html')

@main.route('/home')
def home():
    if 'user' not in session:
        return redirect(url_for('main.login'))
    return render_template('home.html', user=session['user'])

@main.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('main.login'))
