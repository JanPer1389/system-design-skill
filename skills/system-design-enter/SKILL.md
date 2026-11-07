---
name: system-design-enter
description: Use when a system architecture request needs routing between requirements discussion, review and implementation planning.
---

# Enter System Design

**Core principle:** choose the requested outcome from evidence, not a mandatory pipeline. Read [shared policies](references/policies.md) and [the operating method](references/methodology.md). Conceptual name: `system-design:enter`; portable ID: `system-design-enter`.

## Route once, then continue

1. **Establish the brief.** Read the request, available decisions and repository rules. Identify the requested artifact and scope. Completion: you can state what the user needs answered.
2. **Classify the evidence.** Prompt-first means a business request, possibly no code; code-first means partial implementation; existing project means substantial implementation. Name actual sources/limits. These are contexts, not stages.
3. **Choose the operation.** Explore desired behavior/boundaries ? `system-design-brainstorm`; assess current/proposed architecture ? `system-design-review`; prepare execution instructions ? `system-design-plan`. Service decomposition/distributed consistency adds `system-design-microservices` to review/plan.
4. **Check the plan gate.** Missing established architectural decisions **OR** missing code-grounded understanding requires review. Without code, review requirements/proposed design once and state implementation absence. A plan request authorizes review ? plan. Reuse sufficient current inspection; name new grounds for a refresh.
5. **Hand the brief forward.** State the action briefly, load the chosen skill and carry requirements/decisions/evidence into it. Completion: the operation produces its artifact or reaches a specific material blocker; enter does not restart itself.

Sibling paths are `../<portable-ID>/SKILL.md`. Resolve host IDs through [host tools](references/host-tools.md); use native loading or the installed file path. Use [the reference index](references/reference-index.md) to select conditional subjects rather than load the whole library.

## Boundaries and stop conditions

A review-only request ends with review. A plan request does not force brainstorm when defensible assumptions suffice. Brainstorm followed by requested planning confirms the consolidated design first. Stopping questions does not approve open choices.

If essential evidence/capability is missing, state the limitation and continue unaffected work. Outside brainstorm ask only about a blocking material decision. Red flags: routing all requests through all skills; treating discussion as code inspection; repeating review without changed scope/evidence; invoking an already active specialization. Correct the gate/route rather than restart the conversation.
