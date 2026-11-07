CREATE TABLE bookings (
  id TEXT PRIMARY KEY,
  slot_id TEXT NOT NULL,
  student_id TEXT NOT NULL,
  status TEXT NOT NULL
);
-- No uniqueness constraint is declared for confirmed slot ownership here.
