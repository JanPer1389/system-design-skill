# From relationships to mechanisms and frameworks

Use after [domain discovery](domain-discovery.md) and [relationship classification](context-relationships.md). The business relationship supplies the constraints; a mechanism satisfies some of them; a framework supplies implementation facilities. Do not reverse that order.

## Selection procedure

1. Identify caller, authority, state owner and the invariant crossing the edge.
2. Establish same-process versus remote execution from the current architecture/actual requirements. A domain boundary does not require a network boundary.
3. Specify command/query/fact, response timing, permissible staleness and transaction scope.
4. Walk normal execution, concurrent/repeated intent, timeout ambiguity and recovery. Identify what evidence is static and what would need a later runtime check.
5. Compare a direct public module call with alternatives. Add mediation, asynchronous delivery or orchestration only for a named need.
6. Inspect the project's actual stack and configured versions. Consider an existing compatible framework before adding one; record the operational and dependency cost. This skill proposes additions in a plan and never installs them.

Completion: an edge has a defensible mechanism plus explicit guarantees and limits, with no guarantee attributed merely to a tool name.

## Mechanism choices

| Requirement/relationship | Smallest useful mechanism | Evidence needed / failure cost |
| --- | --- | --- |
| One module needs another's answer now | Public application interface, direct call | Dependency direction, allowed input/output, shared or separate transaction |
| Consumer needs insulation from supplier vocabulary | Adapter/ACL at the consuming boundary | Translate business meanings and failure states; do not pass supplier ORM entities throughout |
| Many consumers need a stable shared contract | OHS plus published schemas/vocabulary | Contract ownership, compatible evolution and failure representation; REST/gRPC is a subsequent transport choice |
| An accepted fact triggers independent local reactions | In-process event dispatch when losing work on process crash is acceptable, otherwise a durable mechanism | Listener order, transaction timing, handler failures, durable recovery if required |
| A committed write must eventually produce an external message | Transactional Outbox with a relay, if a single local atomic write can contain state and publication record | Relay retries, duplicate publish, ordering scope and cleanup; consumers still need repeat handling |
| Repeated delivery must not repeat an effect | Durable deduplication/Inbox or naturally idempotent mutation | Identity, retention, atomic effect plus record, concurrent duplicate behavior |
| Multiple local transactions form a long-running business process | Explicit process manager/orchestrator; Saga only when compensation is meaningful | Durable state, deadlines, partial completion, irreversibility and manual recovery |
| A caller needs a fast view of several owners' data | Query composition first; projection/read model if justified | Freshness, rebuild/backfill, missing data and authorization; not automatically CQRS/Event Sourcing |
| A write requires one immediate invariant | Keep the authoritative transaction local where possible | If splitting it, explain the changed guarantee, coordination cost and failure model |

For Outbox mechanics see the pattern author's [transactional outbox](https://microservices.io/patterns/data/transactional-outbox.html). Do not promise exactly-once effects from an at-least-once delivery mechanism.

## Framework fit: facilities, not architecture proofs

The following are examples for an already compatible stack, not a technology shortlist to impose. Verify APIs/configuration against the project's pinned version when writing exact signatures.

| Existing stack / candidate | Useful facility for an established relationship | What it does not establish |
| --- | --- | --- |
| Java/Spring: Spring Modulith | Describes application modules and their exposed interfaces/dependencies; can support module interaction | That the domain boundaries are correct or that separate services are needed |
| TypeScript/NestJS: `@nestjs/cqrs` | Command/query/event handling facilities; event-to-command process composition | That business compensation, durable Saga state or delivery guarantees have been implemented |
| Workflow stack: Temporal | Durable workflow execution and managed workflow state across long-running work | That a business action or an Activity's external side effect is repeat-safe by default |
| Python/SQLAlchemy ORM | Session/transaction facilities that can participate in a local Unit of Work | That a shared engine means shared Session, or that arbitrary concurrent tasks may share it safely |
| HTTP ecosystem: OpenAPI | Describes a language-neutral HTTP API surface for producers/consumers | That meanings, business invariants or runtime compatibility are correct |
| Internal RPC ecosystem: gRPC/Protocol Buffers | Typed service contracts and request/streaming facilities where those requirements matter | Cross-service transactions, idempotency or justification for decomposition |
| Messaging ecosystem: RabbitMQ | Delivery mechanisms with producer/consumer reliability choices | Atomicity with the application's database or exactly-once business effects |

Primary sources: [Spring Modulith fundamentals](https://docs.spring.io/spring-modulith/reference/fundamentals.html), [NestJS CQRS](https://docs.nestjs.com/recipes/cqrs), [Temporal execution](https://docs.temporal.io/workflow-execution), [SQLAlchemy sessions](https://docs.sqlalchemy.org/en/20/orm/session_basics.html), [OpenAPI](https://www.openapis.org/what-is-openapi), [gRPC concepts](https://grpc.io/docs/what-is-grpc/core-concepts/), [RabbitMQ reliability](https://www.rabbitmq.com/docs/reliability). These references do not authorize application network calls or dependency changes. If docs/tools are unavailable, avoid version-specific claims and mark the capability unverified.

## Inspect what actually realizes the guarantee

For any claimed framework-based pattern, trace registration/wiring → caller → state mutation → transaction/delivery boundary → handler → error/recovery path. A dependency declaration shows availability, not usage; a decorator shows a hook, not the full invariant. Read configuration and version constraints as text. Read tests as intended behavior, not successful execution.

For an ACL, inspect a semantic translation, not only serialization. For a local Unit of Work, inspect Session lifetime and commit ownership. For a claimed Saga, inspect persisted process state, compensation decisions, retries and unrecoverable states; an RxJS stream or class named Saga does not prove those mechanics. For a claimed Outbox, find the local atomic write and relay, not just an events table.

Record the recommendation as `edge → invariant → mechanism → framework facility (if any) → configuration/code evidence → missing guarantee → verification to hand off`. Use [architecture patterns](architecture-patterns.md) if the choice changes system structure, and [design patterns](design-patterns.md) for the local component design.
