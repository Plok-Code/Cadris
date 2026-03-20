"""One-shot migration: add billing columns to users table.

Run from the control-plane directory:
    python migrate_add_billing.py

Safe to re-run — skips columns that already exist.
"""

import sqlite3
import sys
from pathlib import Path

DB_PATH = Path(__file__).parent / "data" / "cadris-dev.db"

COLUMNS = [
    ("name", "TEXT"),
    ("stripe_customer_id", "TEXT"),
    ("plan_expires_at", "TEXT"),
    ("missions_this_month", "INTEGER DEFAULT 0"),
    ("month_reset_at", "TEXT"),
]


def migrate():
    if not DB_PATH.exists():
        print(f"DB not found at {DB_PATH} — nothing to migrate (will be created on first run).")
        return

    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()

    # Get existing columns
    cursor.execute("PRAGMA table_info(users)")
    existing = {row[1] for row in cursor.fetchall()}

    added = 0
    for col_name, col_type in COLUMNS:
        if col_name in existing:
            print(f"  [skip] {col_name} already exists")
            continue
        sql = f"ALTER TABLE users ADD COLUMN {col_name} {col_type}"
        print(f"  [add]  {sql}")
        cursor.execute(sql)
        added += 1

    # Add unique index on stripe_customer_id (SQLite can't do UNIQUE on ALTER TABLE)
    try:
        cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS ix_users_stripe_customer_id ON users(stripe_customer_id)")
        print("  [idx]  unique index on stripe_customer_id")
    except Exception as e:
        print(f"  [skip] index: {e}")

    # Update existing 'core' plans to 'free'
    cursor.execute("UPDATE users SET plan = 'free' WHERE plan = 'core'")
    updated = cursor.rowcount

    conn.commit()
    conn.close()

    print(f"\nDone: {added} columns added, {updated} users updated (core -> free).")


if __name__ == "__main__":
    print("Migrating billing columns...")
    migrate()
