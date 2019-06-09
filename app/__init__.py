from flask import Flask, render_template
app = Flask(__name__)

@app.route('/login')
def login_route():
    return render_template('usercontrol/login.html') 
    
@app.route('/')
def landing():
    return render_template('landingpage/index.html')

@app.route('/register')
def register_route():
    return render_template('usercontrol/register.html')