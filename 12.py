import random
import time
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  
socketio = SocketIO(app)
STOCKS = {'AAPL': 150.0, 'GOOGL': 2800.0, 'TSLA': 700.0}
@app.route('/')
def index():
    return render_template('index.html')
def update_stock_prices():
    while True:
        stock = random.choice(list(STOCKS.keys()))
        change = random.uniform(-1, 1)
        STOCKS[stock] = round(STOCKS[stock] + change, 2)
        socketio.emit('update', {stock: STOCKS[stock]})
        time.sleep(1)
@socketio.on('connect')
def handle_connect():
    print('Client connected')
@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')
if __name__ == '__main__':
    socketio.start_background_task(update_stock_prices)
    socketio.run(app, debug=True)