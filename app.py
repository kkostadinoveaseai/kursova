from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import os

app = Flask(__name__)


def get_db():
    return mysql.connector.connect(
        host=os.environ.get('DB_HOST', 'db'),
        user=os.environ.get('DB_USER', 'root'),
        password=os.environ.get('DB_PASSWORD', 'rootpassword'),
        database=os.environ.get('DB_NAME', 'testdb')
    )


@app.route('/')
def index():
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT id, content, created_at FROM notes ORDER BY id DESC')
        notes = cursor.fetchall()
        conn.close()
        return render_template('index.html', notes=notes, error=None)
    except Exception as e:
        return render_template('index.html', notes=[], error=str(e))


@app.route('/add', methods=['POST'])
def add():
    content = request.form.get('content', '').strip()
    if content:
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute('INSERT INTO notes (content) VALUES (%s)', (content,))
            conn.commit()
            conn.close()
        except Exception:
            pass
    return redirect(url_for('index'))


@app.route('/delete/<int:note_id>', methods=['POST'])
def delete(note_id):
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM notes WHERE id = %s', (note_id,))
        conn.commit()
        conn.close()
    except Exception:
        pass
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)