from flask import Flask, render_template, request, redirect, url_for, session
import jwt
import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Dummy user data
users = {
    "user1": "password1"
}

def generate_token(username):
    payload = {
        'username': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    token = jwt.encode(payload, app.secret_key, algorithm='HS256')
    return token

def verify_token(token):
    try:
        payload = jwt.decode(token, app.secret_key, algorithms=['HS256'])
        return payload['username']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

@app.route('/')
def index():
    token = session.get('token')
    if token and verify_token(token):
        return render_template('main.html')
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            token = generate_token(username)
            session['token'] = token
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('token', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)