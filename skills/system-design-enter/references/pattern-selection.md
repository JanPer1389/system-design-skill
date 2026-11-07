# Selecting architectural mechanisms

Express a decision as requirement → constraints → viable options → choice → consequences → revisit condition. Prefer a short decision relevant to the task over a pattern catalog.

First select the level of decision. Use [domain discovery](domain-discovery.md) for responsibilities and invariant ownership; [context relationships](context-relationships.md) for model/dependency relationships; [relationship mechanisms](relationship-mechanisms.md) for contracts, communication and compatible framework facilities; [design patterns](design-patterns.md) for local collaborations; [architecture patterns](architecture-patterns.md) for organization, data and deployment choices. The tables below are starting positions, not conclusions about an uninspected project.

| Concern | Starting position | Evidence that can justify more |
| --- | --- | --- |
| Structure | Small application; modular monolith for a server | Independent deployment, isolation, ownership or load |
| Layers | Clear responsibilities and dependency direction | A useful boundary around rules or variability |
| API | HTTP resources and explicit commands as needed | gRPC for strict internal contracts/streaming; GraphQL for actual read needs |
| Persistence | Relational data for related transactional facts | Query/data shape requiring JSON, denormalization or another store |
| ORM | Explicit transaction and session lifetimes | Repository/Unit of Work where they add a useful boundary |
| History | Snapshots or revisions | Events genuinely serving as the authoritative source for Event Sourcing |
| Concurrency | Atomic changes, appropriate session isolation, version checks | Short critical locks or justified distributed coordination |
| Workflow | States and sequential steps | Independent branches for DAG; durable long-running orchestration; compensation for Saga |
| Queues | Smallest reliable processing mechanism | Delivery, routing, scheduling or scale requirements for a broker |
| Cache | No cache without a reason | Expensive repeat reads plus an explicit freshness/invalidation policy |

Verify mechanics: a shared engine is not necessarily a shared ORM session; History is not Event Sourcing; separate read/write functions are not CQRS; editing a result is not a human decision gate; job states alone do not establish a workflow engine. Use primary technical documentation and disclose version/limits when needed; fetching documentation does not authorize application integration calls.

Before naming a pattern as present, identify its participants, controlling invariant and actual interaction in the inspected sources. Before recommending it, identify the gap it addresses and the extra cost. If either cannot be shown, keep it an unverified hypothesis or omit it. A technology option is not an architectural decision until its fit to the established relationship is explained.
