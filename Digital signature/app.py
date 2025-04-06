from flask import Flask, render_template, request, redirect, url_for, session, flash
import json, os
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from ds_core import DigitalSignature

app = Flask(__name__)
app.secret_key = 'supersecretkey'

USERS_FILE = 'users.json'
HISTORY_FILE = 'history.json'


for file in [USERS_FILE, HISTORY_FILE]:
    if not os.path.exists(file):
        with open(file, 'w') as f:
            json.dump({}, f)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        with open(USERS_FILE, 'r') as f:
            users = json.load(f)

        user = users.get(username)
        if user and check_password_hash(user['password'], password):
            session['username'] = username
            users[username]['last_login'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            with open(USERS_FILE, 'w') as f:
                json.dump(users, f, indent=4)
            return redirect(url_for('dashboard'))
        flash("Invalid credentials")
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        with open(USERS_FILE, 'r') as f:
            users = json.load(f)

        if username in users:
            flash("Username already exists!")
            return redirect(url_for('signup'))

        users[username] = {
            'password': generate_password_hash(password),
            'last_login': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        with open(USERS_FILE, 'w') as f:
            json.dump(users, f, indent=4)
        flash("Signup successful. Please login.")
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/logout')
@login_required
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    username = session['username']
    with open(HISTORY_FILE, 'r') as f:
        history = json.load(f)
    with open(USERS_FILE, 'r') as f:
        users = json.load(f)
    user_history = history.get(username, [])
    last_login = users[username].get("last_login", "N/A")
    total_signatures = sum(len(v) for v in history.values())
    total_users = len(users)
   
    verified_messages = total_signatures  

    return render_template(
        "dashboard.html",
        username=username,
        last_login=last_login,
        total_signed=len(user_history),
        total_signatures=total_signatures,
        verified_messages=verified_messages,
        total_users=total_users
    )


@app.route('/sign', methods=['GET', 'POST'])
@login_required
def sign():
    signed_message = None
    if request.method == 'POST':
        message = request.form['message']
        ds = DigitalSignature()
        ds.load_keys()
        signed_message = ds.sign_message(message).hex()

        with open(HISTORY_FILE, 'r') as f:
            history = json.load(f)
        history.setdefault(session['username'], []).append({
            "message": message,
            "signature": signed_message,
            "timestamp": datetime.now().isoformat()
        })
        with open(HISTORY_FILE, 'w') as f:
            json.dump(history, f, indent=4)

    return render_template('sign.html', signed_message=signed_message)

@app.route('/verify', methods=['GET', 'POST'])
@login_required
def verify():
    result = None
    if request.method == 'POST':
        message = request.form['message']
        signature = bytes.fromhex(request.form['signature'])
        ds = DigitalSignature()
        ds.load_keys()
        result = ds.verify_signature(message, signature)
    return render_template('verify.html', result=result)

@app.route('/history')
@login_required
def history():
    with open(HISTORY_FILE, 'r') as f:
        data = json.load(f)
    user_history = data.get(session["username"], [])
    return render_template("history.html", history=user_history)

if __name__ == '__main__':
    app.run(debug=True)



