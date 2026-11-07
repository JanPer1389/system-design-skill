# Design patterns: prove the mechanism

Use when assigning responsibilities inside a module or evaluating an existing abstraction. **Start with the variation or rule that needs protection.** Then trace collaboration between concrete components. Keep simple functions and explicit conditionals when they express the current need more clearly.

## Investigation and selection

1. Identify the caller's contract, changing behavior and invariant.
2. Inspect current implementations/callers and a working example in the project.
3. Compare the existing design with a direct function/object design and a candidate pattern.
4. State the mechanism that distinguishes the pattern, its additional indirection and its failure/lifecycle implications.
5. Choose only the relevant abstraction; record the evidence and revisit condition. In a plan identify the exact public interface and a behavioral test; in review state what is observed, absent or uncertain.

Completion: every pattern claim describes participants, collaboration and protected behavior; removing the pattern name would still leave an understandable explanation.

## Behavioral and structural patterns

| Pattern | Use when / mechanism to inspect | Common false positive or cost |
| --- | --- | --- |
| Strategy | One contract has interchangeable algorithms selected by policy or caller | A group of unrelated helper functions; unnecessary interfaces for one stable algorithm |
| State | Legal behavior/transitions depend on an explicit lifecycle state | A status enum without transition ownership or guarded operations |
| Adapter | A boundary translates an incompatible interface into the consumer's contract | Renaming methods while leaking supplier semantics; use a real ACL if model meanings differ |
| Facade | A stable narrow capability hides a subsystem's collaboration | A pass-through layer over every class with no simpler client contract |
| Decorator | A wrapper preserves the wrapped contract while adding a composed responsibility | An inheritance hierarchy with changed semantics; hidden retry/caching effects |
| Observer / publish-subscribe | A subject's fact notifies independent subscribers | Assuming durable/external delivery from local callbacks; unbounded subscriber coupling |
| Command | An operation becomes a value that can be passed or handled explicitly | A method ending in Command; durability and authorization remain separate decisions |
| Factory | Creation needs variation, validation or lifecycle ownership behind a contract | Mechanical constructors hidden behind a factory for each type |
| Specification | A reusable business predicate is composed and evaluated deliberately | Every boolean expression wrapped in a class; query translation must preserve semantics |

## Domain and persistence patterns

| Pattern | Evidence to trace | Design consequence / limit |
| --- | --- | --- |
| Entity / Value Object | Identity through change versus attribute-based equality; local validity rules | Choose by business semantics, not ORM annotation |
| Aggregate / root | Controlled mutation and invariants across a meaningful consistency boundary | A collection navigation or foreign key is not sufficient evidence |
| Repository | A domain/application-facing persistence boundary with purposeful collection-like operations | Wrapping every ORM method can add indirection without isolating anything |
| Unit of Work | Explicit lifetime groups affected operations into the intended commit/rollback boundary | Shared engine/global client does not establish one transaction |
| Domain Service | A business rule spans concepts but has no natural entity owner | Avoid an anemic collection of unrelated procedures named Service |
| Application Service | Orchestrates a use case, authority checks and transaction boundaries | Keep domain policy ownership clear; avoid inventing a layer for a trivial tool |

Dependency injection is a construction/wiring technique; it can support several designs without proving any particular one. DTOs are boundary data shapes, not evidence of rich domain modeling. A persistence record and a public contract may intentionally differ.

## Test the design on paper

For fictional HarborDesk, a pricing Strategy is justified if the same quote operation has genuinely different pricing algorithms and callers need the same contract. If only one fixed rate exists, a function may suffice. A Booking State design is useful when transitions carry permissions/invariants; a state name alone adds no protection.

For either choice ask: who creates it, who chooses behavior, who may mutate it, how errors propagate, and what repeats do? A retry Decorator must not silently duplicate a non-idempotent charge. A cache Decorator must define freshness and authorization scope. The pattern can be structurally present and still be inappropriate for the requirements.

Use [domain discovery](domain-discovery.md) for model boundaries and [architecture patterns](architecture-patterns.md) for system/deployment choices. Do not mix a local Strategy with architectural CQRS or a service topology: they solve different levels of problem.
