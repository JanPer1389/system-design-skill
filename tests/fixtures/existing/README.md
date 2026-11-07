# Workshop system

A server application serves staff and customers. Its modules handle bookings and billing in one process. PostgreSQL holds related transactional data. Staff confirmation must not double-book a slot. Payments are delegated to a provider; settled payment notifications may arrive more than once.

Review source only. The fixture is not a runnable application; no credentials or database are provided.
