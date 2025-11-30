import os
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime

# App setup
app = Flask(__name__, static_folder="../static", template_folder="../templates")
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret")

# Mongo setup
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/dsapp")
client = MongoClient(MONGO_URI)
db = client.get_default_database() if client else client.dsapp
users = db.users
topics = db.topics

# Helper
def current_user():
    uid = session.get("user_id")
    if not uid:
        return None
    return users.find_one({"_id": ObjectId(uid)})

# Routes
@app.route("/")
def index():
    return render_template("index.html", user=current_user())

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.form
        if users.find_one({"email": data['email']}):
            flash('Email already registered', 'danger')
            return redirect(url_for('register'))
        hashed = generate_password_hash(data['password'])
        uid = users.insert_one({
            'name': data.get('name',''),
            'email': data['email'],
            'password': hashed,
            'created_at': datetime.utcnow()
            }).inserted_id
        session['user_id'] = str(uid)
        flash('Registered successfully', 'success')
        return redirect(url_for('dashboard'))
    return render_template('register.html') 

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        data = request.form
        user = users.find_one({'email': data['email']})
        if user and check_password_hash(user['password'], data['password']):
            session['user_id'] = str(user['_id'])
            flash('Logged in', 'success')
            return redirect(url_for('dashboard'))
        flash('Invalid credentials', 'danger')
        return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out', 'info')
    return redirect(url_for('index'))