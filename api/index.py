import os
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime

# App setup
app = Flask(__name__, static_folder="../static", template_folder="../templates")
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret")