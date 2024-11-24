from flask import Flask, render_template, request, redirect, url_for
import sqlite3
app = Flask(__name__)
DATABASE = 'inventory.db'
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn
@app.route('/')
def index():
    conn = get_db_connection()
    items = conn.execute('SELECT * FROM items').fetchall()
    conn.close()
    return render_template('index.html', items=items)
@app.route('/add', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']
        conn = get_db_connection()
        conn.execute('INSERT INTO items (name, quantity) VALUES (?, ?)', (name, quantity))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add_item.html')
@app.route('/edit/<int:item_id>', methods=['GET', 'POST'])
def edit_item(item_id):
    conn = get_db_connection()
    item = conn.execute('SELECT * FROM items WHERE id = ?', (item_id,)).fetchone()
    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']
        conn.execute('UPDATE items SET name = ?, quantity = ? WHERE id = ?', (name, quantity, item_id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    conn.close()
    return render_template('edit_item.html', item=item)
@app.route('/delete/<int:item_id>', methods=['POST'])
def delete_item(item_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM items WHERE id = ?', (item_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))
def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            quantity INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
if __name__ == '__main__':
    init_db()
    app.run(debug=True)