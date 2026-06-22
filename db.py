"""Выбор бэкенда БД: SQLite или PostgreSQL.

Какой бэкенд использовать — задаётся в config.ini:

    [database]
    backend = sqlite      # или postgres

Приоритет настроек: переменные окружения > config.ini > значения по умолчанию.
Поддерживаемые переменные окружения (удобно для деплоя/секретов):
    DB_BACKEND     — sqlite | postgres
    DATABASE_PATH  — путь к файлу SQLite
    DATABASE_URL   — строка подключения PostgreSQL

Различия диалектов спрятаны здесь:
    * connect()     — открыть соединение (строки доступны по имени колонки);
    * PLACEHOLDER   — '?' для SQLite, '%s' для PostgreSQL.
Поэтому app.py и init_db.py не зависят от конкретной СУБД.
"""

import configparser
import os

_HERE = os.path.dirname(os.path.abspath(__file__))

_cfg = configparser.ConfigParser()
_cfg.read(os.path.join(_HERE, "config.ini"), encoding="utf-8")

BACKEND = (
    os.environ.get("DB_BACKEND")
    or _cfg.get("database", "backend", fallback="sqlite")
).strip().lower()

if BACKEND == "postgres":
    DSN = os.environ.get("DATABASE_URL") or _cfg.get(
        "database",
        "postgres_dsn",
        fallback="postgresql://postgres:postgres@db:5432/guestbook",
    )
    PLACEHOLDER = "%s"
else:
    _path = os.environ.get("DATABASE_PATH") or _cfg.get(
        "database", "sqlite_path", fallback="guestbook.db"
    )
    # Относительный путь считаем от папки проекта, а не от текущего каталога.
    SQLITE_PATH = _path if os.path.isabs(_path) else os.path.join(_HERE, _path)
    PLACEHOLDER = "?"


def connect():
    """Открыть соединение с выбранной БД. Строки доступны по имени колонки."""
    if BACKEND == "postgres":
        import psycopg
        from psycopg.rows import dict_row

        return psycopg.connect(DSN, row_factory=dict_row)

    import sqlite3

    conn = sqlite3.connect(SQLITE_PATH)
    conn.row_factory = sqlite3.Row
    return conn
