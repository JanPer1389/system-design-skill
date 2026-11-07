# Fictional HarborDesk

The product rents rooms. A member requests a room/time slot, staff confirms it, and only one confirmed booking may hold the slot. Reservations uses Customer to mean the attendee with access rights. Billing uses Customer to mean the legal payer; one payer may pay for several unrelated attendees. Billing may finish payment collection after confirmation. Notifications sends informational updates; losing a notification must not release a room or alter a charge.

One small team currently maintains one server and one relational database. No independent load, security-isolation or release need is known. Reservation confirmation and billing have different business rules, but the deployment model is not decided by the number of nouns. The user asks for a domain model that preserves immediate slot exclusivity and tolerates eventual billing updates. Existing package directories are named api, services and repositories.
