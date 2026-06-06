from flask import current_app, g
from psycopg import connect
from psycopg.rows import dict_row


def get_db():
    if "db" not in g:
        database_url = current_app.config.get("DATABASE_URL", "")
        if not database_url:
            raise RuntimeError("DATABASE_URL is not configured. Set it in your environment before starting the app.")

        g.db = connect(_normalize_database_url(database_url), row_factory=dict_row)
    return g.db


def close_db(_error=None) -> None:
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db() -> None:
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS analysis_history (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                language TEXT NOT NULL DEFAULT 'Python',
                submitted_code TEXT NOT NULL,
                status TEXT NOT NULL,
                source TEXT NOT NULL,
                analysis_mode TEXT NOT NULL DEFAULT 'Standard',
                error_type TEXT NOT NULL,
                issue TEXT NOT NULL,
                solution TEXT NOT NULL,
                explanation TEXT NOT NULL,
                fixed_code TEXT NOT NULL,
                improvements_json TEXT NOT NULL,
                time_complexity TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
        )
        _ensure_column(cursor, "analysis_history", "language", "TEXT NOT NULL DEFAULT 'Python'")
        _ensure_column(cursor, "analysis_history", "analysis_mode", "TEXT NOT NULL DEFAULT 'Standard'")
    db.commit()


def fetch_one(query: str, params: tuple = ()):
    with get_db().cursor() as cursor:
        cursor.execute(query, params)
        return cursor.fetchone()


def fetch_all(query: str, params: tuple = ()):
    with get_db().cursor() as cursor:
        cursor.execute(query, params)
        return cursor.fetchall()


def execute(query: str, params: tuple = (), commit: bool = False):
    with get_db().cursor() as cursor:
        cursor.execute(query, params)
        row_id = cursor.fetchone()["id"] if cursor.description else None
    if commit:
        get_db().commit()
    return row_id


def _ensure_column(cursor, table: str, column: str, definition: str) -> None:
    cursor.execute(
        """
        SELECT 1
        FROM information_schema.columns
        WHERE table_name = %s AND column_name = %s
        """,
        (table, column),
    )
    if cursor.fetchone() is None:
        cursor.execute(f"ALTER TABLE {table} ADD COLUMN {column} {definition}")


def _normalize_database_url(url: str) -> str:
    if url.startswith("postgres://"):
        return "postgresql://" + url[len("postgres://"):]
    return url
