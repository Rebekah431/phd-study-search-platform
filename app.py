from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS studies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            university TEXT NOT NULL,
            subject TEXT NOT NULL,
            location TEXT NOT NULL,
            funding TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/', methods=['GET'])
def index():
    query = request.args.get('query')
    subject = request.args.get('subject')

    conn = get_db_connection()

    if query:
        studies = conn.execute(
            "SELECT * FROM studies WHERE title LIKE ? OR university LIKE ?",
            ('%' + query + '%', '%' + query + '%')
        ).fetchall()
    elif subject:
        studies = conn.execute(
            "SELECT * FROM studies WHERE subject = ?",
            (subject,)
        ).fetchall()
    else:
        studies = conn.execute("SELECT * FROM studies").fetchall()

    conn.close()
    return render_template('index.html', studies=studies)

@app.route('/add', methods=('GET', 'POST'))
def add_study():
    if request.method == 'POST':
        title = request.form['title']
        university = request.form['university']
        subject = request.form['subject']
        location = request.form['location']
        funding = request.form['funding']

        if not title or not university:
            return "Title and University are required"

        conn = get_db_connection()
        conn.execute(
            "INSERT INTO studies (title, university, subject, location, funding) VALUES (?, ?, ?, ?, ?)",
            (title, university, subject, location, funding)
        )
        conn.commit()
        conn.close()
        return redirect('/')

    return render_template('add_study.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
