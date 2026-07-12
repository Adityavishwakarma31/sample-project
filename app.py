import os
import time
from flask import Flask, jsonify, request
import psycopg2
from psycopg2 import OperationalError

app = Flask(__name__)

# Database connection settings (environment variables se aayenge, jo tum `docker run -e` se pass karoge)
DB_HOST = os.environ.get('DB_HOST', 'db')
DB_NAME = os.environ.get('DB_NAME', 'mydatabase')
DB_USER = os.environ.get('DB_USER', 'postgres')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'postgres')
DB_PORT = os.environ.get('DB_PORT', '5432')


def get_db_connection(retries=5, delay=3):
    """DB se connect karta hai, thodi retries ke saath (kyunki DB container start hone mein time leta hai)"""
    for attempt in range(retries):
        try:
            conn = psycopg2.connect(
                host=DB_HOST,
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD,
                port=DB_PORT
            )
            return conn
        except OperationalError as e:
            print(f"DB connect attempt {attempt + 1} failed: {e}")
            time.sleep(delay)
    raise Exception("Database se connect nahi ho paya")


def init_db():
    """Table banata hai agar exist nahi karti"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id SERIAL PRIMARY KEY,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    cur.close()
    conn.close()


@app.route('/')
def home():
    return jsonify({
        "message": "Hello from Flask running inside Docker! 🐳",
        "status": "success"
    })


@app.route('/about')
def about():
    return jsonify({
        "project": "Simple Flask Docker App with Postgres",
        "description": "Yeh ek dockerized Flask + Postgres application hai"
    })


@app.route('/messages', methods=['GET'])
def get_messages():
    """Sab messages database se fetch karo"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, content, created_at FROM messages ORDER BY id DESC")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    messages = [
        {"id": r[0], "content": r[1], "created_at": str(r[2])}
        for r in rows
    ]
    return jsonify({"messages": messages})


@app.route('/messages', methods=['POST'])
def add_message():
    """Naya message database mein insert karo"""
    data = request.get_json()
    content = data.get('content')

    if not content:
        return jsonify({"error": "content field zaroori hai"}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO messages (content) VALUES (%s) RETURNING id",
        (content,)
    )
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"id": new_id, "content": content, "status": "created"}), 201


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
