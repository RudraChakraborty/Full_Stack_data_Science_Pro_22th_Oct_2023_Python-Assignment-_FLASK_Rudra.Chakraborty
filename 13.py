import time
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)
@app.route('/')
def index():
    return render_template('index.html')
def send_notifications():
    notifications = [
        "New user joined!",
        "System update scheduled.",
        "New message received!",
        "Reminder: Meeting at 3 PM."
    ]
    while True:
        for notification in notifications:
            socketio.emit('notification', {'message': notification})
            time.sleep(5)
@socketio.on('connect')
def handle_connect():
    print("Client connected")
    socketio.start_background_task(send_notifications)
@socketio.on('disconnect')
def handle_disconnect():
    print("Client disconnected")
if __name__ == '__main__':
    socketio.run(app, debug=True)
