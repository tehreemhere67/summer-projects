import sqlite3
import random
import string
from flask import Flask
from flask import redirect

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("urls.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS urls (
            short_code TEXT PRIMARY KEY,
            original_url TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def generate_short_code():
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for _ in range(6))

def save_url(short_code, original_url):
    conn = sqlite3.connect("urls.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO urls (short_code, original_url) VALUES (?, ?)", (short_code, original_url))
    conn.commit()
    conn.close()

@app.route("/shorten/<path:url>")
def shorten(url): #so when i go on web and search root url/shorten/xyz url i put here, this function runs, the xyz url is passed to it, it generates a random 6 digit code, save it in database with the xyz url i had put there when searching on the web 
    short_code = generate_short_code()
    save_url(short_code, url)
    return f"Short URL created: 127.0.0.1:5000/{short_code}" #now visiting 127.0.0.1:5000/{short_code} should redirect me to the page at xyz url mentioned above (the original url)

@app.route("/<short_code>")
def redirect_to_url(short_code):
    conn = sqlite3.connect("urls.db")
    cursor = conn.cursor()
    cursor.execute("SELECT original_url FROM urls WHERE short_code = ?", (short_code,))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return redirect(result[0])
    else:
        return "Short URL not found", 404


if __name__ == "__main__":
    init_db()
    app.run(debug=True)