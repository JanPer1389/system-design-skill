# Plan method: decisions an implementer cannot infer

**Core principle:** write for an engineer who has not seen this repository or conversation. They can write idiomatic code once the exact interface, rules and proving behavior are known. The plan must transfer those decisions, not transcribe the entire future application.

The plan is a handoff. Commands and implementation steps in it are instructions for a later executor. The author does not execute them, create application scaffolding or start an implementation workflow.

## Phase 1 — Establish the source and close the review gate

Collect the goal, source requirements/design/review, explicit user decisions, repository rules and current implementation evidence. Apply the shared OR gate: missing architectural decisions or missing code-grounded understanding requires review first. For no code, review the intended design once and state implementation absence. Reuse a relevant current review with its source/scope/revision; a discussion alone is not inspection.

If this plan follows brainstorm, obtain consolidated-design confirmation. Otherwise proceed with defensible assumptions; ask only about an unresolved material decision preventing continuation. Completion: source documents and decision status are explicit, and the gate's basis is recorded without a recursive review loop.

## Phase 2 — Establish the system map, target and file responsibilities

Build three connected levels before task decomposition:

1. **System map:** goals/non-goals, participants, domain responsibilities, data owners, critical workflows/invariants and external dependencies. Distinguish the inspected current state from a prompt-only proposed model.
2. **Target solution:** components, dependency directions, contracts, deployment shape, storage and tool/stack choices. Independently assess whether the supplied design meets requirements; it is not automatically the target. Use [stack assessment](stack-assessment.md) to compare retaining/improving the current approach with credible alternatives. Explain the selected solution, change costs and rejected alternatives. Preserve justified architecture and explicit binding constraints; do not reduce planning to patching the author's design. Do not introduce unrelated modernization or force distribution.
3. **Implementation:** exact directory/file responsibilities, types/interfaces, state transitions, migration and independently verifiable tasks implementing that target.

Trace each scoped need through a target decision and contract to owning tasks and acceptance checks. Use a compact traceability table where helpful. All consequential technical choices are agent-owned by default; ask only about blocking business/external constraints. A plan-only request does not acquire a brainstorm confirmation loop. A plan following brainstorm still requires the agreed consolidated-design gate. Surface conflicts with explicit binding decisions rather than silently changing them.

Apply [diagram guidance](diagrams.md) under the shared triggers. Keep current and target views distinct and align diagram names/edges with task interfaces.

If the request contains independent subsystems, make their boundaries and ordering explicit. Separate plans only where each can deliver a meaningful coherent result; do not stall an authorized combined plan for a process preference.

Inspect existing conventions and exact symbols. Map directories/files before tasks. Group things that change for the same business reason; give each file a clear responsibility and a public contract. Retain architecture and patterns that satisfy the needs. Change boundaries, tools or responsibilities when concrete requirements, coupling, reliability or maintenance costs justify it; explain the improvement and transition. A familiar file tree or a user suggestion is not sufficient justification in either direction.

Use [domain discovery](domain-discovery.md) when boundaries are unclear, [relationships](context-relationships.md) and [mechanisms](relationship-mechanisms.md) when contracts cross owners, and [pattern selection](pattern-selection.md) for alternative designs. Completion: every proposed file exists for a stated responsibility; each dependency has a direction and contract owner.

## Phase 3 — Define shared constraints and interfaces once

Begin the plan with:

- Goal/status and source design/review links; whole-system map and current-state limits.
- Target architecture and actual/proposed stack, decision rationale, alternatives and migration cost.
- Requirement → decision/contract → task → acceptance-check traceability.
- Global constraints: exact agreed values, compatibility, dependency restrictions, naming and operational requirements. Separate assumptions from binding decisions.
- Directory/file responsibilities.
- Contracts/types/errors/state transitions, ownership, transaction and repeat/concurrency semantics.
- Task dependency order, independent deliverables and shared-file conflicts.
- Review focus: relevant input/failure classes implied by requirements that the straightforward happy path misses.

For each review-focus item identify its owning task and behavioral check. Do not create a ceremonial fixed number of risks or leave a risk list unconnected to tasks. If a topic is inapplicable, explain briefly rather than invent a migration, broker or new layer.

Completion: neighboring tasks agree on names, types, error semantics and lifecycle before their steps are written.

## Phase 4 — Size tasks around independent outcomes

A task is the smallest meaningful deliverable with its own verification cycle. Fold setup/configuration/documentation into the deliverable that needs them. Split tasks when one can be accepted while another legitimately needs changes. Do not split arbitrary file edits that cannot be verified until a later task secretly completes them.

Each task includes:

1. **Result/requirement:** a concrete change in observable behavior or an explicit nonexecutable deliverable.
2. **Files:** exact Create / Modify / Test paths; verified existing symbols/locations; say none where applicable. Do not invent future line numbers.
3. **Interfaces:** consumes/produces, exact signatures/input-output types, errors and dependencies on other task contracts. Name the task providing any fixture/type/helper.
4. **Checkable steps:** one action with one completion condition per checkbox.
5. **Semantics:** relevant atomicity, same/new intent, concurrent attempts, failure/recovery and migration impact.
6. **Verification/acceptance:** command, working directory and expected observation; what proves the task's requirement.

Completion: an implementer can work from this task and its explicitly named dependencies without inventing a consequential interface or business rule.

## Phase 5 — Write executable-behavior steps in TDD order

Unless the user explicitly chooses otherwise:

1. Write the behavioral test: exact name/path, concrete state/action/assertions with agreed values; show the significant excerpt.
2. Run the focused command from a stated directory and confirm the expected missing-behavior failure. A broken interpreter, missing unrelated dependency or fixture typo is not the intended red result.
3. Implement the minimum change: exact signature/file, essential values, algorithm only where the contract/tests leave ambiguity. The executor writes routine bodies.
4. Run the focused and relevant regression checks, naming expected results and invariants.
5. Refactor where useful and verify again; preserve behavior/contracts.

An explicit user override changes the sequence and must be recorded. Documentation/nonexecutable work gets a meaningful content/link/schema check, not a manufactured failing test. A verification step says what command to run and what observation means success; the author never says it has already passed.

Use [the worked plan excerpt](planning-example.md) for appropriate specificity. Avoid both extremes: vague "add appropriate tests" and complete application implementations hidden in code blocks.

## Phase 6 — Carry consistency and evolution through the tasks

For affected changing operations establish:

| Concern | Plan must decide |
| --- | --- |
| Authority | Who may decide and write; how callers receive rejection |
| Atomicity | Which writes/effects belong to one local transaction; where it begins/ends |
| Repeated intent | Identity/scope/retention; original result, rejection or other explicit repeat behavior |
| New intent | Why a deliberate new action remains independently meaningful |
| Concurrency | Competing requests, invariant enforcement, uniqueness/version/lock strategy and conflict mapping |
| Partial failure | Commit/response ambiguity, duplicate publication, recovery/compensation owner |
| Migration | Existing data validity, backfill/constraints, old/new versions, failure and rollback limits |

Distribute these decisions to owning tasks and their tests; do not repeat generic idempotency advice without a concrete operation. Keep authoritative invariants local where possible. Outbox/Inbox/Saga require a justified mechanism; consult the microservices specialization only when needed.

## Phase 7 — Self-review as the recipient

Read the source requirements again, then the completed plan:

1. **Coverage and target quality:** independently challenge the proposed target, not just its fidelity to the author. Trace every scoped requirement through the system map, target decision/contract, owning task and acceptance check. Check that justified tool/architecture improvements are carried into tasks and constraints are respected. Add missing tasks or explicitly record an unresolved blocker.
2. **Step scan:** every step decides a checkable action; remove vague placeholders and routine full bodies that decide nothing further.
3. **Type consistency:** compare signatures, property names, values and errors across task boundaries. Verify each referenced symbol/fixture is existing or assigned to a task.
4. **Review focus:** every material failure/input class has an owning check; distinguish planned coverage from existing test evidence.
5. **Consistency/evolution:** examine repeats, concurrency, migrations, compatibility and failure recovery across tasks, not only within each one.
6. **Dependency/conflict scan:** verify order, independent tasks and files that must not be edited concurrently.
7. **Proportion:** keep enough detail for an unambiguous implementation without turning the plan into the full program.

Correct supported issues in the document before handoff. If a material product decision is missing, surface that decision; a polished plan cannot conceal it. Completion: source coverage is traceable and a recipient can implement without inventing consequential choices.

## Handoff and red flags

Show the substantive plan to the user through an available native plan presentation or chat, from the system map and target decisions down to all implementation tasks and checks. Do not return only a link, outline or executive summary. Plan Mode is not required; do not pretend to switch modes. Save the same plan in the shared directory when permitted, link the copy and state any save failure. Split into coherent numbered parts and continue delivery if output limits require it. Respect explicit presentation preferences. State remaining assumptions/limitations and stop planning. Preserve an already specified execution process, but do not automatically assign agents, worktrees, commits, deployment or an implementation skill.

Red flags: a file link replacing the delivered plan; a system diagram unconnected to tasks; unquestioned adoption of a suggested architecture; asking the user to choose SDKs; invented file locations; types/fixtures no task defines; commands without expected results; future checks called passing; every noun becoming a module/service; shared-file conflicts ignored; TDD applied against an explicit override; a plan longer mainly because it contains routine application bodies. Correct the responsible phase rather than restart the whole pipeline.
