from flask import Flask, render_template, request, redirect, url_for, session
import jwt
import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Dummy user data
users = {
    "user1": "password1",
    "user2" :"pasword2"
}
tokenwebsockets = {
    "user1": "token1",
    "user2" :"token2"
}

def generate_token(username):
    payload = {
        'username': username,
        'exp': datetime.datetime.now() + datetime.timedelta(hours=1)
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
    tokenuser = session.get('tokenwebsocket')
    username = session.get('username')
    ipClient = request.remote_addr
    ipServer = request.host


    if token and verify_token(token):
        return render_template('main.html', username=username , tokenwebsocket=tokenuser,
                               ipClient=ipClient,ipServer=ipServer,ipServer2=ipServer)
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print (f'username: {username}, password: {password}')
        if username in users and users[username] == password:
            token = generate_token(username)
            session['token'] = token
            session['username'] = username
            session['tokenwebsocket'] = tokenwebsockets[username]

            return redirect(url_for('index'))
        else:
            return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('token', None)
    return redirect(url_for('login'))





# Custom error pages
@app.errorhandler(400)
@app.errorhandler(401)
@app.errorhandler(403)
@app.errorhandler(404)
@app.errorhandler(500)
@app.errorhandler(502)
@app.errorhandler(503)
def handle_error(error):
    return render_template("error.html", errorcode=error.code), error.code

@app.route('/trigger/<int:error_code>')
def trigger_error(error_code):
    """Manually trigger an error by visiting /trigger/404, /trigger/500, etc."""
    if error_code in [400, 401, 403, 404, 500, 502, 503]:
        return render_template("error.html", errorcode=error_code), error_code
    else:
        return "Unknown error code. Try 400, 401, 403, 404, 500, 502, or 503.", 400


if __name__ == '__main__':
    app.run(debug=True)