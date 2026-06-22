"""Мини-приложение «Гостевая книга» на Flask + SQLite.

Две задачи демонстрации:
  * GET  /      — показать все записи из БД
  * POST /add   — добавить новую запись в БД

На сервере приложение запускается через gunicorn (см. LESSON_PLAN.md),
а не через app.run() — этот блок нужен только для локальной разработки.
"""

import os
import sqlite3

from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

# Путь к файлу БД. На сервере можно переопределить через переменную окружения,
# например: export DATABASE_PATH=/var/data/guestbook.db
DATABASE = os.environ.get("DATABASE_PATH", "guestbook.db")


def get_db() -> sqlite3.Connection:
    """Открыть соединение с БД. row_factory=Row даёт доступ по имени колонки."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def index():
    conn = get_db()
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
        conn = get_db()
        conn.execute(
            "INSERT INTO entries (name, message) VALUES (?, ?)",
            (name, message),
        )
        conn.commit()
        conn.close()
    return redirect(url_for("index"))


@app.route("/health")
def health():
    """Простой эндпоинт проверки, что приложение живо."""
    return {"status": "ok"}


if __name__ == "__main__":
    # ВНИМАНИЕ: это только для локального запуска (python app.py).
    # На сервере используем gunicorn — см. план занятия.
    app.run(host="0.0.0.0", port=8000, debug=True)
