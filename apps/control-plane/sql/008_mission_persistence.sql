-- Migration 008: Add persistence columns for mission state tracking
-- Allows resuming missions after browser refresh or navigation away.

ALTER TABLE missions ADD COLUMN phase TEXT DEFAULT 'intake';
ALTER TABLE missions ADD COLUMN current_wave INTEGER DEFAULT 0;
ALTER TABLE missions ADD COLUMN qualification_answers_json TEXT DEFAULT '{}';
