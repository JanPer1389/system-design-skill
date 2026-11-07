# Discover domains before drawing components

Use for a new business idea, an unclear domain model, a disputed responsibility or a change spanning several areas. Existing modules are evidence about the current implementation, not automatically the correct domain boundaries.

**Result:** a capability map, a small glossary, important invariants and candidate bounded contexts with reasons. A bounded context is a boundary within which a model and its vocabulary have a coherent meaning; it need not be a deployed service. See [Fowler's bounded-context explanation](https://martinfowler.com/bliki/BoundedContext.html).

## 1. Discover decisions, not nouns alone

Collect goals, actors, permissions, important commands and successful outcomes from the brief, examples and inspected code. For each workflow ask internally: who requests it, who decides, what changes, what must remain true, who sees the result? Follow read-only code paths to locate that decision today. A list of database tables is insufficient because tables do not explain authority or business purpose.

For fictional HarborDesk, "member", "room" and "invoice" are candidate concepts. "May this booking become confirmed?" and "Which legal party owes this invoice?" reveal different decision responsibilities. Record terminology collisions: a customer can mean an attendee in reservations and a billed legal party in billing. Do not force one universal Customer model across those meanings.

Completion: each important workflow has an actor, decision owner, outcome and at least its key invariant. Unknown behaviors are labeled rather than filled in as settled requirements.

## 2. Group business capabilities

Group decisions by shared purpose, rules and change drivers. Distinguish:

- **Core subdomain:** the part delivering the project's differentiating value; the user/business context determines it.
- **Supporting subdomain:** necessary business-specific work that supports the core.
- **Generic subdomain:** broadly available capability, where reuse or a commodity service may be sufficient.

These categories guide investment, not automatic service counts or framework choice. In a tiny tool a sophisticated strategic model may add no value; use plain responsibilities when sufficient. Ask business questions only in brainstorm or for a material blocker elsewhere.

Completion: candidate capabilities are named by what the business accomplishes, with examples of decisions inside and outside each.

## 3. Propose bounded contexts from model consistency

For each candidate context record:

| Field | What to establish |
| --- | --- |
| Purpose | Which decisions this context owns |
| Language | Meaning of key terms here; translations at boundaries |
| State ownership | Authoritative writes and lifecycle, including deletion |
| Rules/invariants | What must be true immediately; what may converge later |
| Public capabilities | Commands, queries and facts other contexts may use |
| Dependencies | Inputs consumed, upstream authority, expected freshness |
| Change drivers | What tends to change together and what must evolve independently |
| Evidence/status | Current code, user decision, proposed boundary or unknown |

Look for reasons to split: conflicting meanings, independent policy authority, different lifecycle/security constraints or actual independent release/load needs. Look for reasons to merge: the same decision needs constant coordination, no coherent independent model exists, or a strict local invariant spans the proposed boundary. Directory count and team count alone do not settle this.

Completion: each boundary has a positive responsibility and a reason; its dependencies can be mapped using [context relationships](context-relationships.md).

## 4. Identify entities, values and consistency boundaries

An **entity** preserves identity through changes. A **value object** is described by its attributes and rules rather than a separate identity. An **aggregate** groups state whose business invariants are protected through a controlled root. These are candidate design choices, not mandatory classes.

For each relationship between concepts distinguish identity reference, ownership/lifecycle, cardinality, optionality and changing business role. A one-to-many database relation does not prove one aggregate; an object composition does not prove one transaction. Locate the write authority and determine whether the invariant is enforced by transaction, constraint, atomic operation or a carefully specified eventual process.

Example: a room can have many historical bookings, while a particular slot has at most one confirmed holder. Historical cardinality is one-to-many; the live exclusivity rule needs its own enforcement analysis. An invoice can refer to a booking ID without sharing its aggregate or delete lifecycle.

Completion: state-changing operations name the affected consistency boundary and repeat intent, or explicitly identify the missing information.

## 5. Challenge and record the map

Walk one normal, one repeated and one failing scenario across the proposed boundaries. If every operation needs mutual internal access, revisit the split. If one context must imitate another's model everywhere, investigate whether a translation boundary is missing or the split is artificial. Compare to a modular monolith before recommending deployment separation.

Write a compact domain section: capabilities/glossary → contexts/owners → entity/value/invariant model → relationships → unresolved decisions. For a review distinguish current topology from the proposed target. For a plan link each target boundary to file responsibilities and tasks. For brainstorm present the user-visible implications and confirm decisions without requiring the user to choose DDD terminology.

Further primary guidance: [Microsoft domain analysis](https://learn.microsoft.com/en-us/azure/architecture/microservices/model/domain-analysis). Apply its boundary-analysis ideas to the actual application; reading a microservices example is not a requirement to build microservices.
