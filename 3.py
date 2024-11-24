from flask import Flask, render_template
app = Flask(__name__)
@app.route('/greet/<name>')
def greet(name):
    return render_template('greeting.html', name=name)
if __name__ == '__main__':
    app.run(debug=True)