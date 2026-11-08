# Reference selection

Read references at the point their branch is reached. A larger library is not a reason to load every document. Start with the current skill's mandatory method, then open the subject needed to settle an actual decision. Record unknowns rather than guessing around missing evidence.

| Trigger in the current task | Read | Produce/check |
| --- | --- | --- |
| Any System Design operation | [policies](policies.md), [methodology](methodology.md) | Scope, evidence/decision ledger and completion gate |
| Business responsibility, ambiguous vocabulary, entity or ownership boundary | [domain discovery](domain-discovery.md) | Capability map, terms, invariants, candidate contexts |
| More than one context/module/external party interacts | [context relationships](context-relationships.md) | Directional relationship map; authority and coupling |
| Choosing how an established relationship works in code/runtime | [relationship mechanisms](relationship-mechanisms.md) | Contract, consistency, failure behavior; optional framework fit |
| Local object/component responsibilities or variation | [design patterns](design-patterns.md) | Mechanism-level pattern evidence and smallest useful design |
| Dependency/deployment style, read/write structure or evolution strategy | [architecture patterns](architecture-patterns.md) | Drivers, alternatives, trade-offs, revisit condition |
| Comparing candidate patterns | [pattern selection](pattern-selection.md) | Requirement-to-decision record, not a catalog |
| Review, including required review before plan | [review method](review-method.md), [report contract](review-report.md) | Two independent verdicts, evidence, calibrated findings |
| Interactive requirements/design exploration | [question rounds](question-rounds.md) | Dependency-aware rounds, alternatives, builder check |
| Detailed implementation handoff | [planning method](planning-method.md) | File/interface/task decomposition and self-review |
| A handoff needs a concrete level-of-detail example | [planning example](planning-example.md) | Exact test/signature/commands without a full implementation |
| New/adapted file tree | [fictional project tree](project-tree.md) | Responsibilities and dependency rules, not copied scaffolding |
| Loader/tool names or unavailable capability | [host tools](host-tools.md) | Native supported action or explicit limitation |

The five topics domain discovery, context relationships, relationship mechanisms, design patterns and architecture patterns describe different levels. An entity association is not an organizational relationship. An organizational relationship is not a transport protocol. A framework is not proof that an architectural pattern exists. Move between levels by stating the invariant and evidence that justify the move.

For material technology decisions read [stack assessment](stack-assessment.md): evidence, agent-owned choices, official-source verification and migration cost. For requested drawings, substantial work needing a visual explanation, or a sufficiently understood prompt-only model read [diagram guidance](diagrams.md): Mermaid views, evidence/status labels and rendering limits. These apply to every operation without changing its scope.
