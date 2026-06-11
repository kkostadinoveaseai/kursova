from flask import Flask, render_template, request, jsonify
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
        cursor.execute('SELECT expression, result, created_at FROM history ORDER BY id DESC LIMIT 20')
        history = cursor.fetchall()
        conn.close()
    except Exception:
        history = []
    return render_template('index.html', history=history)


@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    expression = data.get('expression', '')
    try:
        allowed = set('0123456789+-*/.() ')
        if not all(c in allowed for c in expression):
            raise ValueError('Invalid characters')
        result = eval(expression)
        result = round(float(result), 10)
        result = int(result) if result == int(result) else result
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO history (expression, result) VALUES (%s, %s)',
                (expression, str(result))
            )
            conn.commit()
            conn.close()
        except Exception:
            pass
        return jsonify({'result': str(result)})
    except ZeroDivisionError:
        return jsonify({'error': 'Деление на нула'})
    except Exception:
        return jsonify({'error': 'Грешка'})


@app.route('/history/clear', methods=['POST'])
def clear_history():
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM history')
        conn.commit()
        conn.close()
    except Exception:
        pass
    return jsonify({'ok': True})


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)