from flask import Flask, render_template
from .config import AUTH_SQLITE_URI
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = AUTH_SQLITE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(1000))

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

db.create_all()

@app.route('/login')
def login_route():
    return render_template('usercontrol/login.html') 
    
@app.route('/')
def landing():
    return render_template('landingpage/index.html')

@app.route('/register')
def register_route():
    return render_template('usercontrol/register.html')