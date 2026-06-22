-- Схема для PostgreSQL (backend = postgres в config.ini).
-- Применяется скриптом init_db.py.

CREATE TABLE IF NOT EXISTS entries (
    id         SERIAL PRIMARY KEY,
    name       TEXT NOT NULL,
    message    TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT now()
);
