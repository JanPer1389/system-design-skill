# Review report contract and calibration example

Use after completing [the review method](review-method.md). This is the output shape, not a substitute for inspection. Write in the user's language. Fill fields with evidence or explicitly mark unknown/not applicable; do not leave template placeholders in the delivered artifact.

## Required content

1. **Scope and basis:** requested area/result, requirements and decisions, source documents/files, revision/local differences, mode and limitations. State whether implementation exists and that analysis is static.
2. **Architecture and flows:** concise whole-project map, then scoped responsibilities, domain boundaries, relationships, state owners and key workflows. Distinguish current structure from proposed target.
3. **Requirements compliance:** supported status for scoped requirements; identify Missing/Extra/Misunderstood and Cannot verify. For a design-only review, assess internal requirements/design alignment, not implementation compliance.
4. **Strengths and actual patterns:** useful mechanisms with source evidence; state what they achieve and their limits.
5. **Findings:** Critical / Important / Minor, each with stable ID, file/symbol/location or design section, observed mechanism, requirement/invariant, consequence, basis/counter-evidence, confidence and correction options/trade-offs. Empty severity categories can say none.
6. **Unresolved / declined to judge:** unavailable evidence and explicitly set-aside behaviors with reasons and implications for the verdict.
7. **Assessment:** two verdicts plus short reasoning. **Compliance:** Meets scoped requirements / Gaps found / Insufficient evidence. **Architectural quality:** Suitable for scoped goal / Needs changes / Insufficient evidence. A suitable static design is not a runtime guarantee or permission to deploy.

When some scoped requirements can be judged and others cannot, give the supported verdict alongside explicit unknowns. Do not force one cheerful all-clear. For re-review, lead with per-finding statuses, then new breakage, out-of-scope observations and the scoped assessment.

## Fictional example: conditional ownership risk

Assume the **fictional inspected evidence** is a `BookingService.confirm` method in `backend/reservations/application.py` that loads one booking, writes `confirmed` and commits. The inspected `backend/reservations/schema.sql` defines booking primary keys and no confirmed-slot uniqueness rule; relevant callers/constraints beyond these files are unavailable. Requirement R1 says a slot may have only one confirmed holder.

**Strength:** the inspected operation has a visible local transaction boundary. This supports grouping its own writes; it does not establish serialization across different bookings for the same slot.

**F1 — Important, conditional static risk:** `BookingService.confirm` plus the inspected schema do not show enforcement of R1 across competing bookings. If no other constraint or authoritative allocation step exists, concurrent confirmations could violate exclusivity. The finding is conditional because unseen persistence/callers might provide that enforcement. No race was executed or reproduced.

**Options:** enforce the authoritative slot invariant in the local persistence transaction; or make an existing authoritative allocation capability explicit if one already exists. A database uniqueness constraint can reject conflicting writes but requires error mapping and migration; an allocation operation can centralize authority but must still define concurrent attempts. A broker is not a correction for this evidence gap.

**Compliance:** insufficient evidence for R1; inspected sources do not demonstrate enforcement. **Quality:** needs clarification or changes before relying on the confirmation design for R1. **Declined:** runtime behavior and constraints outside supplied sources. Tests may be proposed for a later executor, but none ran during this review.

If a later source reveals a valid database constraint and correct error mapping, update or close F1; do not keep it because the original report sounded convincing. If that source instead proves a direct invariant violation, refine the finding and calibrate severity to the demonstrated consequence.

## Finding self-check

Can the reader locate the source? Does the consequence follow from that mechanism? Did you distinguish source evidence from assumptions and future proposals? Is the suggested correction smaller than a wholesale redesign? Is the same issue duplicated under several pattern names? Have you kept an honest unknown where execution would be required? Correct the report before handing it over.
