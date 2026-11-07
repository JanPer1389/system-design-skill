---
name: system-design-plan
description: Use when the user requests a detailed implementation plan or architecture handoff for another engineer or agent.
---

# Write a system implementation plan

**Core principle:** transfer decisions an engineer cannot infer: exact responsibilities, interfaces, values and checks. A plan is neither a vague task list nor the full application written in advance.

Read [shared policies](../system-design-enter/references/policies.md), [operating method](../system-design-enter/references/methodology.md) and **[planning method](../system-design-enter/references/planning-method.md)**. Use [the worked excerpt](../system-design-enter/references/planning-example.md) to calibrate specificity. Conceptual name: `system-design:plan`; portable ID: `system-design-plan`.

## Planning sequence

1. **Establish sources and the review gate.** Missing architectural decisions **OR** missing code-grounded understanding requires `../system-design-review/SKILL.md`. Discussion alone is insufficient. Without code review requirements/design once, state implementation absence and continue. Reuse current sufficient evidence; do not loop. Brainstorm requires consolidated-design confirmation before this handoff.
2. **Map scope and file responsibilities.** Inspect stack, conventions and exact symbols as text. Group changes by responsibility and coherent deliverables; preserve justified architecture. State each file's ownership before task decomposition. Completion: file structure has reasons and public boundaries.
3. **Define global constraints and contracts.** Link design/review; specify goal/status, architecture, stack, binding values, assumptions, types, errors, state owners and dependencies. Establish transaction/repeat/concurrency semantics. Add review-focus failure/input classes with owning tasks/checks.
4. **Size independently verifiable tasks.** Each includes result/requirement, exact Create/Modify/Test paths, interfaces consumed/produced, named dependencies and checkbox steps with checkable outcomes. Assign each helper/fixture/type to existing code or a task. Identify independent tasks and shared-file conflicts without automatically assigning agents/worktrees/commits.
5. **Write behavior steps in TDD order.** Write concrete test assertions ? run the exact command and confirm expected failure ? implement the minimum specified interface/algorithm ? focused/regression checks ? useful refactoring and recheck. State working directory and expected observation. Record an explicit user override; documentation gets meaningful validation rather than fake failing tests.
6. **Carry evolution through tasks.** Address migration, compatibility, coexistence and recovery where applicable. Put concurrency, duplicate delivery and timeout checks in the task owning the invariant, not generic advice.
7. **Self-review against sources.** Trace requirements to tasks/checks; scan vague steps and excessive bodies; compare types/names/values; check review-focus coverage, consistency semantics, order and file conflicts. Correct supported gaps before handoff.

## Detail and completion

Use [domain discovery](../system-design-enter/references/domain-discovery.md) for unclear responsibilities; [relationships](../system-design-enter/references/context-relationships.md) and [mechanisms/frameworks](../system-design-enter/references/relationship-mechanisms.md) for contracts crossing owners; [pattern selection](../system-design-enter/references/pattern-selection.md) for choices. Activate `../system-design-microservices/SKILL.md` for service concerns, reusing it if active.

Show test assertions, exact signatures and essential algorithm excerpts; leave routine bodies to the executor. Red flags: undefined types, invented line numbers, vague testing instructions, commands without expected results or a program transcript disguised as a plan.

Save/link the plan under the shared plan path with acceptance criteria, assumptions, risks and unknowns. Commands are **unexecuted handoff instructions**. Do not run them, start implementation, change application files/dependencies/infrastructure or ask a redundant execution-method question. Outside brainstorm ask only about a blocking material decision.
