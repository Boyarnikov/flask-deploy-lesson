"""Инициализация базы данных.

Бэкенд берётся из config.ini (см. db.py). В зависимости от него применяется
своя схема: schema.sqlite.sql или schema.postgres.sql.

Запускать на сервере ОДИН раз после установки зависимостей:

    python init_db.py
"""

import os

import db

_HERE = os.path.dirname(os.path.abspath(__file__))

SCHEMA_FILE = {
    "sqlite": "schema.sqlite.sql",
    "postgres": "schema.postgres.sql",
}


def main() -> None:
    schema_name = SCHEMA_FILE.get(db.BACKEND, SCHEMA_FILE["sqlite"])
    with open(os.path.join(_HERE, schema_name), "r", encoding="utf-8") as f:
        sql = f.read()

    conn = db.connect()
    if db.BACKEND == "sqlite":
        conn.executescript(sql)  # sqlite умеет несколько команд за раз
    else:
        conn.execute(sql)  # одна команда CREATE TABLE
    conn.commit()
    conn.close()
    print(f"OK: база ({db.BACKEND}) инициализирована из {schema_name}")


if __name__ == "__main__":
    main()
