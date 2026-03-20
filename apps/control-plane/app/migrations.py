from __future__ import annotations

import logging
from pathlib import Path
from sqlalchemy import text
from sqlalchemy.engine import Engine

logger = logging.getLogger(__name__)


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
                        try:
                            connection.exec_driver_sql(statement)
                        except Exception as exc:
                            # SQLite doesn't support IF NOT EXISTS for ALTER TABLE.
                            # Skip "duplicate column" errors from idempotent migrations.
                            if "duplicate column" in str(exc).lower() or "already exists" in str(exc).lower():
                                logger.info("Skipping (column already exists): %s", statement[:80])
                            else:
                                raise
            connection.execute(
                text("INSERT INTO schema_migrations (filename) VALUES (:filename)"),
                {"filename": path.name},
            )
