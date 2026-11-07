# Binding behavior and a proposed implementation

The user requires that retrying the same payment intent must not charge twice, while a deliberate new payment uses a different intent identity. Timeouts can occur after the provider accepted a charge.

The proposed design tells the implementer to retry each timeout as a brand-new request with a newly generated intent ID. The design author says this is safe because the SDK has built-in retry support. No provider contract, persisted intent record or reconciliation mechanism is supplied. Review the design; do not implement it or call any provider.
