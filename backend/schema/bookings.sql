-- Run this in Supabase SQL Editor (Dashboard -> SQL Editor)
-- Creates the bookings table for the consultant-approval flow

CREATE TABLE IF NOT EXISTS bookings (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  client_name TEXT NOT NULL,
  client_email TEXT NOT NULL,
  consultant_id TEXT NOT NULL,
  consultant_email TEXT NOT NULL,
  booking_date DATE NOT NULL,
  booking_time TIME NOT NULL,
  service TEXT,
  notes TEXT,
  status TEXT NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'confirmed', 'declined')),
  token TEXT UNIQUE NOT NULL,
  calendar_event_id TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_bookings_token ON bookings(token);
CREATE INDEX IF NOT EXISTS idx_bookings_status ON bookings(status);
