# Scoped re-review input

Previous findings:

- F1: the inspected booking schema had no uniqueness rule for the active holder of a slot.
- F2: same-intent versus new-intent identity and repeated effect/result behavior were unspecified in the public confirmation contract.

The author reports that both are fixed. The supplied change only adds the active-slot constraint in review-fixed-schema.sql; the confirmation method remains the supplied existing/application.py. No test execution evidence is supplied. This is a focused static re-review, not a new whole-project audit.
