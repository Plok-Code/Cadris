ALTER TABLE users ADD COLUMN name TEXT;
ALTER TABLE users ADD COLUMN stripe_customer_id TEXT;
ALTER TABLE users ADD COLUMN plan_expires_at TEXT;
ALTER TABLE users ADD COLUMN missions_this_month INTEGER NOT NULL DEFAULT 0;
ALTER TABLE users ADD COLUMN month_reset_at TEXT;
UPDATE users SET plan = 'free' WHERE plan = 'core';
CREATE UNIQUE INDEX IF NOT EXISTS ix_users_stripe_customer_id ON users(stripe_customer_id);
