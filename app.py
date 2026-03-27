from flask import Flask, render_template, request, redirect
import sqlite3
import random
import string

app = Flask(__name__)

# --- Creating a DataBase ---
conn = sqlite3.connect('urls.db')
cursor = conn.cursor()
cursor.execute('''
  CREATE TABLE IF NOT EXISTS urls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    long_url TEXT NOT NULL,
    short_url TEXT NOT NULL
  )
''')
conn.commit()
conn.close()


@app.route('/')
def index():
  return render_template('index.html')

@app.route('/short', methods=["POST"])
def short():
  url = request.form['url']

  # --- Shorted URL ---
  shorted_url = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

  # --- Storing URL and Shorted URL in DB ---
  conn = sqlite3.connect('urls.db')
  cursor = conn.cursor()
  
  cursor.execute('INSERT INTO urls (long_url, short_url) VALUES (?, ?)', (url, shorted_url))
  conn.commit()
  conn.close()

  # Shorted URL
  shorted_url = request.host_url + shorted_url
  
  return render_template("index.html", shorted_url=shorted_url)
  
# Retriving Route
@app.route('/<short_url>')
def retrive(short_url):
  conn = sqlite3.connect("urls.db")
  cursor = conn.cursor()
  cursor.execute("SELECT long_url FROM urls WHERE short_url = ?", (short_url,))
  long_url = cursor.fetchone()[0]
  conn.close()
  
  if long_url:
    return redirect(long_url)
  else:
    return "URL not found"

if __name__ == '__main__':
  app.run(host='127.0.0.1', port=8000, debug=True)
 