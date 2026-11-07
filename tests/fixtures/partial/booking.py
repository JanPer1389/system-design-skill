"""Fixture for static reading only. No external dependencies."""
bookings = []


def request_booking(student, slot):
    bookings.append({"student": student, "slot": slot, "status": "requested"})
    return bookings[-1]
