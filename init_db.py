"""Инициализация базы данных.

Создаёт таблицы из schema.sql. Запускать ОДИН раз на сервере после
установки зависимостей:

    python init_db.py

Файл БД (*.db) намеренно не лежит в репозитории (см. .gitignore) —
именно поэтому базу нужно инициализировать на сервере отдельно.
"""

import os
import sqlite3

DATABASE = os.environ.get("DATABASE_PATH", "guestbook.db")


def main() -> None:
    with open("schema.sql", "r", encoding="utf-8") as f:
        schema = f.read()

    conn = sqlite3.connect(DATABASE)
    conn.executescript(schema)
    conn.commit()
    conn.close()
    print(f"OK: база данных инициализирована -> {DATABASE}")


if __name__ == "__main__":
    main()
