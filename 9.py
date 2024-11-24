from flask import Flask, request, jsonify
import sqlite3
app = Flask(__name__)
DATABASE = 'books.db'
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn
def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            published_year INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
@app.route('/books', methods=['GET'])
def get_books():
    conn = get_db_connection()
    books = conn.execute('SELECT * FROM books').fetchall()
    conn.close()
    return jsonify([dict(book) for book in books])
@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    conn = get_db_connection()
    book = conn.execute('SELECT * FROM books WHERE id = ?', (book_id,)).fetchone()
    conn.close()
    if book is None:
        return jsonify({'error': 'Book not found'}), 404
    return jsonify(dict(book))
@app.route('/books', methods=['POST'])
def create_book():
    data = request.get_json()
    if not all(key in data for key in ('title', 'author', 'published_year')):
        return jsonify({'error': 'Missing required fields'}), 400
    title = data['title']
    author = data['author']
    published_year = data['published_year']
    conn = get_db_connection()
    cursor = conn.execute('INSERT INTO books (title, author, published_year) VALUES (?, ?, ?)', 
                          (title, author, published_year))
    conn.commit()
    new_book_id = cursor.lastrowid
    conn.close()
    return jsonify({'id': new_book_id, 'title': title, 'author': author, 'published_year': published_year}), 201
@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    data = request.get_json()
    if not all(key in data for key in ('title', 'author', 'published_year')):
        return jsonify({'error': 'Missing required fields'}), 400
    title = data['title']
    author = data['author']
    published_year = data['published_year']
    conn = get_db_connection()
    cursor = conn.execute('UPDATE books SET title = ?, author = ?, published_year = ? WHERE id = ?',
                          (title, author, published_year, book_id))
    conn.commit()
    updated = cursor.rowcount
    conn.close()
    if updated == 0:
        return jsonify({'error': 'Book not found'}), 404
    return jsonify({'id': book_id, 'title': title, 'author': author, 'published_year': published_year})
@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    conn = get_db_connection()
    cursor = conn.execute('DELETE FROM books WHERE id = ?', (book_id,))
    conn.commit()
    deleted = cursor.rowcount
    conn.close()
    if deleted == 0:
        return jsonify({'error': 'Book not found'}), 404
    return jsonify({'message': 'Book deleted successfully'})
if __name__ == '__main__':
    init_db()
    app.run(debug=True)