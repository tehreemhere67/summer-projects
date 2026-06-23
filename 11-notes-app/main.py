from flask import Flask, request, session, redirect, render_template
from flask_bcrypt import Bcrypt
import sqlite3

app = Flask(__name__)
app.secret_key = "your-secret-key-here"  # Flask uses this to encrypt session cookies so users can't tamper with them. Just any random string for now, but in real apps this would be kept secret in a .env file.
bcrypt = Bcrypt(app)

def init_db():
    conn = sqlite3.connect("notes.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            content TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    conn.commit()
    conn.close()


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        password_hash = bcrypt.generate_password_hash(password).decode("utf-8")
        
        conn = sqlite3.connect("notes.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, password_hash))
        conn.commit()
        conn.close()
        
        return redirect("/login")
    
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        conn = sqlite3.connect("notes.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()
        
        if user and bcrypt.check_password_hash(user[2], password):
            session["user_id"] = user[0]
            return redirect("/notes")
        else:
            return "Invalid credentials"
    
    return render_template("login.html")
    
@app.route("/notes", methods=["GET"])
def view_notes():
    if "user_id" not in session:
        return redirect("/login")
    
    conn = sqlite3.connect("notes.db")
    cursor = conn.cursor()
    cursor.execute("SELECT content, id FROM notes WHERE user_id = ?", (session["user_id"],))
    notes = cursor.fetchall()
    conn.close()
    
    return render_template("notes.html", notes=notes)

@app.route("/add_note", methods=["POST"]) #not all routes, just like this one, show a page. this just does something and redirects
def add_note():
    if "user_id" not in session:
        return redirect("/login")
    
    note_content = request.form["note"]
    conn = sqlite3.connect("notes.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO notes (user_id, content) VALUES (?, ?)", (session["user_id"], note_content))
    conn.commit()
    conn.close()
    return redirect("/notes")

@app.route("/delete_note", methods=["POST"])
def delete_note():
    if "user_id" not in session:
        return redirect("/login")
    
    note_id = request.form.get("note_id")
    conn = sqlite3.connect("notes.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM notes WHERE id = ? AND user_id = ?", (note_id, session["user_id"]))
    conn.commit()
    
    if cursor.rowcount == 0:
        conn.close()
        return "You don't have permission to delete it."
    
    conn.close()
    return redirect("/notes")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")
      
    
if __name__ == "__main__":
    init_db()
    app.run(debug=True)
