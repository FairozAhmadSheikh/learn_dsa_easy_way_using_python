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


@app.route('/forgot', methods=['GET','POST'])
def forgot():
    if request.method == 'POST':
        email = request.form['email']
        user = users.find_one({'email': email})
        if user:
            # Production: send password-reset email with token
            flash('Password reset link would be sent (configure SMTP)', 'info')
        else:
            flash('Email not found', 'warning')
    return render_template('forgot.html')

@app.route('/dashboard')
def dashboard():
    user = current_user()
    if not user:
        return redirect(url_for('login'))
    cats = topics.distinct('category')
    latest = list(topics.find().sort('created_at', -1).limit(8))
    return render_template('dashboard.html', user=user, categories=cats, latest=latest)

@app.route('/search')
def search():
    q = request.args.get('q','').strip()
    results = []
    if q:
        results = list(topics.find({"$text": {"$search": q}}))
    return render_template('search.html', query=q, results=results)

@app.route('/topics/<category>')
def topics_by_category(category):
    items = list(topics.find({'category': category}))
    return render_template('index.html', category=category, topics=items)

@app.route('/topic/<tid>')
def topic_detail(tid):
    t = topics.find_one({'_id': ObjectId(tid)})
    if not t:
        flash('Topic not found', 'warning')
        return redirect(url_for('dashboard'))
    return render_template('topic_detail.html', topic=t)

# Admin (simple password-protected admin)
@app.route('/admin', methods=['GET','POST'])
def admin_panel():
    admin_pw = os.environ.get('ADMIN_PASSWORD')
    if request.method == 'POST':
        pw = request.form.get('admin_pw')
        if pw != admin_pw:
            flash('Wrong admin password', 'danger')
            return redirect(url_for('admin_panel'))
        # create topic
        title = request.form.get('title')
        category = request.form.get('category')
        content = request.form.get('content')
        topics.insert_one({
                'title': title,
                'category': category,
                'content': content,
                'created_at': datetime.utcnow()
                })
        flash('Topic added', 'success')
        return redirect(url_for('admin_panel'))
    # GET: show admin page
    all_topics = list(topics.find().sort('created_at', -1))
    return render_template('admin.html', topics=all_topics)

# API helper to list categories (example)
@app.route('/api/categories')
def api_categories():
    cats = topics.distinct('category')
    return jsonify(cats)

# For local testing
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))