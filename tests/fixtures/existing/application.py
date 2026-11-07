"""Static fixture: caller supplies transaction and publisher interfaces."""
class BookingService:
    def __init__(self, transaction):
        self.transaction = transaction

    def confirm(self, booking_id):
        with self.transaction() as tx:
            booking = tx.bookings.get(booking_id)
            booking.status = "confirmed"
            tx.bookings.save(booking)


class SagaHistory:
    """The name is deliberately not evidence of Saga or Event Sourcing."""
    def __init__(self):
        self.records = []

    def append(self, message):
        self.records.append(message)
