from __future__ import annotations

from pathlib import Path
from sqlalchemy import text
from sqlalchemy.engine import Engine


def run_sql_migrations(engine: Engine, sql_dir: Path) -> None:
    sql_dir.mkdir(parents=True, exist_ok=True)

    with engine.begin() as connection:
        connection.execute(
            text(
                """
                CREATE TABLE IF NOT EXISTS schema_migrations (
                  filename TEXT PRIMARY KEY,
                  applied_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
        )

        applied = {
            row[0]
            for row in connection.execute(text("SELECT filename FROM schema_migrations")).fetchall()
        }

        for path in sorted(sql_dir.glob("*.sql")):
            if path.name in applied:
                continue

            sql = path.read_text(encoding="utf-8")
            if sql.strip():
                for statement in sql.split(";"):
                    statement = statement.strip()
                    if statement:
                        connection.exec_driver_sql(statement)
            connection.execute(
                text("INSERT INTO schema_migrations (filename) VALUES (:filename)"),
                {"filename": path.name},
            )
