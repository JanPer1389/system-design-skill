---
name: system-design-microservices
description: Use when evaluating service decomposition, domain ownership or consistency and failure behavior across service boundaries during review or planning.
metadata:
  version: "0.2.1"
---

# Evaluate service decomposition

**Core principle:** establish business and consistency boundaries before deployment boundaries. A service is justified by requirements, not an entity name or fashionable framework.

Read [shared policies](../system-design-enter/references/policies.md), [operating method](../system-design-enter/references/methodology.md), **[domain discovery](../system-design-enter/references/domain-discovery.md)** and **[context relationships](../system-design-enter/references/context-relationships.md)**. Conceptual name: `system-design:microservices`; portable ID: `system-design-microservices`.

## Establish the parent operation

This specializes review/plan and keeps their static/nonimplementation boundaries. Direct evaluation uses `../system-design-review/SKILL.md`; a handoff uses `../system-design-plan/SKILL.md`. Mark this specialization active, contribute findings and return without reloading yourself or enter.

## Decomposition sequence

1. **Map responsibility.** Identify domain decisions, vocabulary, entities, invariants and owners from requirements/code/design. Separate current contexts from proposals. Completion: each candidate boundary has a coherent purpose beyond a noun/folder.
2. **Map relationships.** For one service inspect callers, data authority and dependencies; for the whole project map important edges. Separate entity relationships, upstream/downstream model influence and command/query/event flow. Completion: material edges have owners, contract meaning and consistency needs.
3. **Compare deployment choices.** Check whether a modular monolith meets the same need. Evaluate independent load, releases, isolation/security, ownership and operational capacity. Preserve justified existing separation. A user-mandated split is a user constraint, not invented technical necessity.
4. **Choose the smallest viable mechanism.** Read [mechanisms/frameworks](../system-design-enter/references/relationship-mechanisms.md) and [architecture patterns](../system-design-enter/references/architecture-patterns.md). Assign service/data ownership, contracts and local transactions; choose synchronous/asynchronous interaction from timing/failure needs. Do not distribute technical layers mechanically.
5. **Walk failures.** Trace normal completion, duplicate/reordered delivery, concurrent attempts, ambiguous timeout, unavailable dependency and failed recovery. Define intent identity/retention, atomic deduplication/effect, deadlines, bounded retries/backoff, overload and irreversible actions. Completion: each failure has visible state and a recovery owner.
6. **Plan evolution and visibility.** Address compatibility/version coexistence, phased data/traffic migration, temporary shared-storage coupling, rollback/recovery limits, correlation, delivery lag and stuck/failed work. Plan assigns concrete tasks; review identifies gaps/options without implementing them.
7. **Challenge and report.** Compare the choice with the simpler alternative again. Verify each named pattern's mechanics/cost. Return evidence, choices, trade-offs and unknowns to the parent artifact in the shared directories.

## Pattern gates and red flags

Outbox requires a local state-change/publication invariant; Inbox/deduplication requires a duplicate-effect invariant; Saga requires cross-transaction recovery/compensation. Distributed coordination needs an explicit invariant and failure/cost analysis. A broker supplies no business-data atomicity. A Saga-named framework proves neither persistence nor compensation.

Red flags: service per entity, remote hops per technical layer, ambiguous write ownership, unbounded retries without identity, or gRPC/Redis/broker chosen from domain alone. Revisit the affected boundary/mechanism. Do not start services, infrastructure or application code.
