from flask import Flask, render_template, request, flash, url_for, session, redirect
from .config import AUTH_SQLITE_URI, SECRET_KEY
from flask_sqlalchemy import SQLAlchemy
import re
from hashlib import sha256

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = AUTH_SQLITE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = SECRET_KEY

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

@app.route('/login', methods=['GET', 'POST'])
def login_route():
    if request.method == "POST":
        if not request.form['username'] or not request.form['pwd']:
            flash('Please enter all the fields', 'error')
            return render_template("usercontrol/login.html")
        
        pwd_hash = db.session.query(User.password).filter_by(username=request.form['username']).scalar()

        if not pwd_hash:
            flash("No user with such username exists!", "error")
            return render_template("usercontrol/login.html")

        new_pwd_hash = sha256(bytes(request.form['pwd']+SECRET_KEY, "utf-8")).hexdigest()

        if new_pwd_hash != pwd_hash:
            flash("Incorrect password!", "error")
            return render_template("usercontrol/login.html")

        session['loggedin'] = True

        flash("You have been logged in. Welcome back!")
        return redirect(url_for("landing"))
        
    return render_template('usercontrol/login.html') 
    
@app.route('/')
def landing():
    loggedin = True if 'loggedin' in session else False
    return render_template('landingpage/index.html',loggedin=loggedin)

#TODO: Validate shit ton

@app.route('/register', methods=['GET', 'POST'])
def register_route():
    if request.method == 'POST':
        #TODO: Handle emails and usernames that are already being used
        if not request.form['email'] or not request.form['pwd'] or not request.form['confirmpwd']:
            flash('Please enter all the fields', 'error')
            return render_template('usercontrol/register.html')

        if not re.match("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", request.form['email']):
            flash('Invalid email', 'error')
            return render_template('usercontrol/register.html')

        if db.session.query(User.id).filter_by(email=request.form['email']).scalar() is not None:
            flash("E-Mail already exists", 'error')
            return render_template('usercontrol/register.html')

        if request.form['pwd'] != request.form['confirmpwd']:
            flash('Passwords do not match', 'error')
            return render_template('usercontrol/register.html')

        session['email'] = request.form['email']
        session['pwd'] = request.form['pwd']

        return redirect(url_for('register_username'))

    return render_template('usercontrol/register.html')

@app.route('/register_username', methods=['GET', 'POST'])
def register_username():
    if not 'email' in session or not 'pwd' in session:
        return redirect(url_for('landing'))

    if request.method == "POST":
        #TODO: Duplicate username
        if not request.form['username']:
            flash("You need to fill out the username.", "error")
            return render_template('usercontrol/register_username.html')

        if db.session.query(User.id).filter_by(username=request.form['username']).scalar() is not None:
            flash("Username already exists", 'error')
            return render_template('usercontrol/register_username.html')

        pwd_hash = sha256(bytes(session['pwd']+SECRET_KEY, 'utf-8')).hexdigest()

        user = User(request.form['username'], session['email'], pwd_hash)
        
        db.session.add(user)
        db.session.commit()

        flash("You have been successfully registered!")
        return redirect(url_for('landing'))
    return render_template("usercontrol/register_username.html")