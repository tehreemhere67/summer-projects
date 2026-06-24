import sqlite3
from flask import Flask, jsonify, request

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("books.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            year INTEGER NOT NULL
        )
    """)
    conn.commit()
    conn.close()

@app.route("/books", methods=["GET"])
def view_books():    
    conn = sqlite3.connect("books.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    conn.close()

    books_list = [] #need to convert the list of tuples to a list of dictionaries to jsonify
    for book in books:
     books_list.append({
        "id": book[0],
        "title": book[1],
        "author": book[2],
        "year": book[3]
    })
    return jsonify(books_list)

@app.route("/books", methods=["POST"])
def add_book(): 
   data = request.get_json() #convert json data into python dictionary
   title = data["title"]
   author = data["author"]
   year = data["year"] 
 
   conn = sqlite3.connect("books.db")
   cursor = conn.cursor()
   cursor.execute("INSERT INTO books (title, author, year) VALUES (?, ?, ?)", (title, author, year))
   conn.commit()
   conn.close()

   return jsonify({"message": "book added"}), 201 #http response status code

@app.route("/books/<int:id>", methods=["GET"])
def get_book(id):
    conn = sqlite3.connect("books.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books WHERE id = ?", (id,))
    book = cursor.fetchone()
    conn.close()
    
    if not book: #true if book is NONE/nothing fetched since id doesnt exist
        return jsonify({"error": "book not found"}), 404
    
    return jsonify({"id": book[0], "title": book[1], "author": book[2], "year": book[3]})


@app.route("/books/<int:id>", methods=["PUT"])
def update_book(id):
    data = request.get_json()
    conn = sqlite3.connect("books.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE books SET title=?, author=?, year=? WHERE id=?",
                   (data["title"], data["author"], data["year"], id))
    conn.commit()
    if cursor.rowcount == 0:
        conn.close()
        return jsonify({"error": "book not found"}), 404
    conn.close()
    return jsonify({"message": "book updated"}), 200

@app.route("/books/<int:id>", methods=["DELETE"])
def delete_book(id):
    conn = sqlite3.connect("books.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books WHERE id = ?", (id,))
    conn.commit()
    if cursor.rowcount == 0:
        conn.close()
        return jsonify({"error": "book not found"}), 404
    conn.close()
    return jsonify({"message": "book deleted"}), 200  

if __name__ == "__main__":
    init_db()
    app.run(debug=True)