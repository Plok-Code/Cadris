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
                        except Exception as exc:  # noqa: BLE001 — driver errors vary; re-raised if not idempotent
                            msg = str(exc).lower()
                            # Skip known-safe idempotent errors:
                            # - "duplicate column" — SQLite & Postgres duplicate ADD COLUMN
                            # - "already exists"   — Postgres "column X already exists"
                            # - SQLite < 3.35 syntax error on IF NOT EXISTS in ALTER TABLE
                            is_dup = "duplicate column" in msg or "already exists" in msg
                            is_sqlite_if_not_exists = (
                                'near "exists": syntax error' in msg
                                or 'near "if": syntax error' in msg
                            )
                            if is_dup or is_sqlite_if_not_exists:
                                logger.info("Skipping idempotent DDL: %s", statement[:80])
                            else:
                                raise
            connection.execute(
                text("INSERT INTO schema_migrations (filename) VALUES (:filename)"),
                {"filename": path.name},
            )
