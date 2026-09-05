from flask import Flask, jsonify, request
import os
import psycopg
from psycopg.rows import dict_row

app = Flask(__name__)


def get_db_connection():
    return psycopg.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        row_factory=dict_row
    )


@app.route("/")
def home():
    return jsonify({
        "service": "IT Service Desk API",
        "status": "running"
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy"
    })


@app.route("/tickets")
def tickets():
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT id, title, status FROM tickets ORDER BY id;"
                )
                tickets = cursor.fetchall()

        return jsonify(tickets)

    except Exception as error:
        return jsonify({
            "error": str(error)
        }), 500

@app.route("/tickets", methods=["POST"])
def create_ticket():
    try:
        data = request.get_json()

        title = data.get("title")
        status = data.get("status", "Aberto")

        if not title:
            return jsonify({
                "error": "O campo title é obrigatório"
            }), 400

        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO tickets (title, status)
                    VALUES (%s, %s)
                    RETURNING id, title, status;
                    """,
                    (title, status)
                )

                ticket = cursor.fetchone()

        return jsonify(ticket), 201

    except Exception as error:
        return jsonify({
            "error": str(error)
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)