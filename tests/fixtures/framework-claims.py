"""Static fixture only. Names and metadata intentionally overstate architecture."""
declared_dependencies = ["spring-modulith", "nestjs-cqrs", "message-client"]


class SagaFlow:
    def on_booking_confirmed(self, booking):
        return {"action": "email", "booking": booking}


class EventStore:
    def __init__(self):
        self.history = []

    def record_log(self, message):
        self.history.append(message)


class BillingAdapter:
    def adapt(self, upstream_payload):
        return upstream_payload
