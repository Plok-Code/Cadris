-- Migration 009: Persist qualification questions for mission resume
-- Without this, refreshing during qualification leaves the user stuck.

ALTER TABLE missions ADD COLUMN qualification_questions_json TEXT DEFAULT '[]';
