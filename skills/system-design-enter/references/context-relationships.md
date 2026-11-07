# Distinguish and model relationships

Use after identifying candidate contexts, modules or external parties. **First classify the level:** business entities, model ownership, code dependencies and runtime communication are different relationships. Record them separately before connecting them.

## Entity relationships

For each association record cardinality (one/optional/many), identity, lifecycle owner, mutation authority and business role. Distinguish composition (lifecycle ownership), aggregation/reference (independent lifecycle), dependency (uses a capability) and inheritance/subtyping (substitutability). A foreign key establishes referential linkage, not necessarily composition. A subtype must preserve the caller's behavioral contract; similar field names are insufficient.

Keep historical and active-state constraints separate. A member may create many booking requests; a slot can still allow at most one confirmed booking. Record that invariant independently of an ER diagram.

## Context-map relationships

Upstream/downstream describes model/contract influence, not the direction of every HTTP request. Partnership/shared kernel describe collaboration; ACL/conformist describe downstream adaptation; OHS/published language describe the supplier's integration surface. Several can describe the same boundary.

| Relationship | Decision to investigate | Evidence and architectural consequence |
| --- | --- | --- |
| Partnership | Do both owners coordinate success and changes? | Joint contract/release planning; assess coupling and coordination cost |
| Shared Kernel | Is a deliberately small model subset jointly owned? | Agreed ownership/change rules and compatibility tests; a shared utility package alone is not proof |
| Customer/Supplier | Can the downstream negotiate what the upstream supplies? | Explicit contract priorities and change process; distinguish from a powerless consumer |
| Conformist | Does downstream deliberately adopt an upstream model it cannot shape? | Mapping is accepted; document model leakage and switching cost |
| Anti-corruption Layer (ACL) | Must downstream protect its own meanings from upstream concepts? | Translation of semantics, errors and identifiers at its boundary; not merely forwarding JSON |
| Open Host Service (OHS) | Does upstream expose a stable integration capability to multiple consumers? | Supported API, compatibility policy and ownership; protocol choice is a separate decision |
| Published Language | Is the exchange vocabulary explicitly shared? | Versioned schema/semantics and change rules; naming a DTO does not prove semantic agreement |
| Separate Ways | Is integration unnecessary or more costly than duplication? | Intentional independent behavior; document how users complete the overall workflow |

An unstructured entangled model (often called a Big Ball of Mud) is an observation to support with dependency/ownership evidence, not a verdict inferred from folder size. Avoid forcing every pair into one label when the collaboration facts are unavailable. Identify authority/unknowns first.

These context-mapping ideas are grounded in [Microsoft's domain-analysis guidance](https://learn.microsoft.com/en-us/azure/architecture/microservices/model/domain-analysis); the table is an investigation aid, not a checklist demanding all patterns.

## Code and runtime relationships

| Dimension | Questions to settle |
| --- | --- |
| Code dependency | Who imports whose public contract? Are internals/data models bypassed? Is a cycle required or accidental? |
| Command | Who may request a state change, who accepts/rejects it, and how is repeated intent identified? |
| Query | Who owns the answer and freshness guarantee? Can the caller tolerate unavailable/stale data? |
| Event/fact | What has already happened, who owns its meaning, and can consumers receive duplicates or reorderings? |
| Shared state | Who can write, which invariant is jointly protected, and who coordinates schema/lifecycle? |
| Orchestration | Who knows the process state, deadlines, compensation and final outcome? |
| Choreography | Which consumers react independently, and how is end-to-end progress or failure discovered? |

A request/reply protocol can carry a command or query. A broker can carry either commands or facts. Neither HTTP nor messaging determines ownership or consistency. An event-shaped object passed in memory has different failure/durability properties from an externally delivered event.

## Make the relationship explicit

For each important edge produce a compact record:

```text
From / To: Reservations → Billing
Business purpose: request payment authorization for a confirmed offer
Authority: Reservations owns slot allocation; Billing owns payment state
Model relationship: downstream translation if provider meanings differ
Contract: request identity, booking reference, amount/currency, accepted/rejected result
Consistency: state what is immediate and what may be pending
Repeat/failure: same intent, new intent, timeout ambiguity, duplicate notification
Evolution: owner, compatible additions, breaking-change migration
Evidence/status: inspected source, user decision, proposal, or unknown
```

This example is fictional and not a recommendation to distribute Reservations and Billing. After identifying the edge, use [relationship mechanisms](relationship-mechanisms.md) to choose its implementation. Completion: important edges have direction, ownership, contract meaning, consistency and failure semantics; unknown dimensions remain visible.
