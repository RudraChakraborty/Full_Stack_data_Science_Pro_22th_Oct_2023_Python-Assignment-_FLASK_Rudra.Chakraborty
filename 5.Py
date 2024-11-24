from flask import Flask, render_template, request, redirect, url_for, session
app = Flask(__name__)
app.secret_key = 'supersecretkey'
@app.route('/')
def login():
    return render_template('login.html')
@app.route('/setname', methods=['POST'])
def setname():
    username = request.form['username']
    session['username'] = username
    return redirect(url_for('welcome'))
@app.route('/welcome')
def welcome():
    if 'username' in session:
        username = session['username']
        return render_template('welcome.html', username=username)
    else:
        return redirect(url_for('login'))
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))
if __name__ == '__main__':
    app.run(debug=True)
