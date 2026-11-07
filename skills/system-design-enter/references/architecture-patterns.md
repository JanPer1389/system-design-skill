# Architecture patterns: drivers, trade-offs and evidence

Use when evaluating system organization, dependency rules, consistency structure or evolution. Architecture is judged against requirements and operating constraints. A directory layout is one piece of evidence, not the architecture itself.

## Decision procedure

1. Name the driver: business invariant, scale, release independence, isolation, integration or change frequency. Distinguish a measured requirement from a guess.
2. Map the current responsibility, state owner and dependency direction; preserve justified existing choices.
3. Compare the smallest sufficient architecture with the credible alternative. For a new server start with a modular monolith; a local CLI may need fewer boundaries.
4. Walk an important write, a read, a repeated request and a partial failure. Identify transactions, model translations and who owns recovery.
5. Record benefits, costs, migration/compatibility, unsupported guarantees and the condition that would justify reconsideration.

Completion: the chosen style can be explained as a response to concrete drivers, and the main workflow still has an intelligible owner and failure model.

## Organization and dependency styles

| Style | When it helps | Evidence of the mechanism | Cost / reason not to add |
| --- | --- | --- | --- |
| Modular monolith | Coherent server with useful domain boundaries and shared deployment | Modules expose capabilities, protect internals and have understandable dependency direction | Boundaries can erode; enforce where valuable without distributing prematurely |
| Layered architecture | Stable separation of transport, application/domain decisions and persistence | Dependencies and responsibilities actually follow the intended rule | Mere api/services/repository folders add no guarantee; horizontal coupling can dominate changes |
| Ports and adapters / hexagonal | Domain/use cases must be insulated from external technologies | Application-owned ports, concrete adapters, composition at the edge | One interface per class without variability adds overhead |
| Clean/onion variants | A project needs explicit inward dependency rules and separated policy | Core policy independent of outer infrastructure, with boundary translation | Diagram labels alone do not prove dependency inversion; do not force a full layer stack |
| Vertical slices | Changes align around use cases/features across technical concerns | Feature-owned behavior, clear shared foundations and contracts | Duplicated business invariants across slices need attention |
| Microservices | Independent isolation, delivery/ownership or workload requirements justify remote boundaries | Service/data ownership, versioned contracts and operational recovery | Network/consistency/operations costs; use the microservices specialization before recommending |

These styles can coexist. A modular monolith can use vertical slices and ports/adapters. Calling one a replacement for all the others confuses deployment boundaries with dependency organization. See [Fowler's trade-off analysis](https://martinfowler.com/articles/microservice-trade-offs.html) for why distribution requires a contextual cost/benefit decision.

## Data and interaction patterns

| Pattern | Driver / required mechanics | False recognition / trade-off |
| --- | --- | --- |
| Event-driven interaction | Independent reactions to facts; explicit producer/consumer semantics | A broker dependency is not evidence of business decoupling; inspect duplicates/order/recovery |
| CQRS | Meaningfully distinct command and query models/paths solve an actual complexity or scale need | Separate CRUD methods are insufficient; a projection introduces freshness/rebuild concerns if used |
| Event Sourcing | Authoritative persisted events reconstruct state with deliberate evolution rules | An audit/history log is not the source of truth; replay and schema evolution add cost |
| Transactional Outbox / Inbox | Local commit-to-publication and duplicate-effect invariants | An event table without atomic write/relay or deduplication without atomic effect is incomplete |
| Saga / process manager | A multi-step business process crosses local transactions and needs explicit recovery/compensation | A job status table or event stream alone is insufficient; irreversible effects need an honest recovery policy |
| Cache-aside / materialized view | Expensive repeated reads or read composition justify derived state | Define freshness, invalidation and rebuild; do not make cache authoritative accidentally |
| Strangler migration | A boundary can be moved incrementally while old/new behavior coexist | Requires routing, ownership, compatibility and a convergence plan; not a big-bang rewrite label |

Outbox/Inbox/Saga are consistency/workflow patterns, not standalone whole-system deployment styles. Use [relationship mechanisms](relationship-mechanisms.md) to place them on actual edges. A system may use CQRS without Event Sourcing, or events without either. Do not infer the bundle from one term or framework.

## Compare alternatives with the same scenario

For fictional HarborDesk, ask how two simultaneous confirmations compete for one slot. A local database invariant may satisfy it in one modular deployment. Moving confirmation and slot ownership to separate services creates a new consistency problem; "microservices scale" is not an answer to that invariant. Conversely, documented security isolation for untrusted processing can justify a service boundary even if a reference tree shows one backend.

For each alternative state: authoritative write, immediate guarantee, stale/pending state, repeat identity, failure visibility, recovery owner and operational cost. Show what changes for callers during migration. If a critical guarantee cannot be maintained, surface the trade-off or ask about the materially different behavior; do not imply a framework restores it automatically.
