CREATE TABLE bookings (
  id TEXT PRIMARY KEY,
  slot_id TEXT NOT NULL,
  student_id TEXT NOT NULL,
  status TEXT NOT NULL
);
CREATE UNIQUE INDEX one_active_holder
  ON bookings(slot_id)
  WHERE status = 'confirmed';
