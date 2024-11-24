from flask import Flask, render_template
from flask_socketio import SocketIO, send
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)
@app.route('/')
def chat():
    return render_template('chat.html')
@socketio.on('message')
def handle_message(message):
    print(f'Received message: {message}')
    send(message, broadcast=True)
if __name__ == '__main__':
    socketio.run(app, debug=True)