"""Мини-приложение «Гостевая книга» на Flask.

Бэкенд базы данных (SQLite или PostgreSQL) выбирается в config.ini — вся
работа с СУБД спрятана в db.py, поэтому здесь код одинаков для обоих движков.

  * GET  /      — показать все записи
  * POST /add   — добавить новую запись
  * GET  /health — проверка + текущий бэкенд БД

На сервере приложение запускается через gunicorn (см. LESSON_PLAN.md).
"""

from flask import Flask, redirect, render_template, request, url_for

import db

app = Flask(__name__)


@app.route("/")
def index():
    conn = db.connect()
    entries = conn.execute(
        "SELECT name, message, created_at FROM entries ORDER BY id DESC"
    ).fetchall()
    conn.close()
    return render_template("index.html", entries=entries)


@app.route("/add", methods=["POST"])
def add():
    name = request.form.get("name", "").strip() or "Аноним"
    message = request.form.get("message", "").strip()
    if message:
        conn = db.connect()
        conn.execute(
            f"INSERT INTO entries (name, message) "
            f"VALUES ({db.PLACEHOLDER}, {db.PLACEHOLDER})",
            (name, message),
        )
        conn.commit()
        conn.close()
    return redirect(url_for("index"))


@app.route("/health")
def health():
    """Удобно проверить, какой бэкенд БД сейчас активен."""
    return {"status": "ok", "backend": db.BACKEND}


if __name__ == "__main__":
    # Только для локальной разработки. На сервере — gunicorn.
    app.run(host="0.0.0.0", port=8000, debug=True)
