---
name: system-design-review
description: Use when assessing a proposed system design, partial implementation, existing application architecture or changes to architectural contracts.
metadata:
  version: "0.3.2"
---

# Review system architecture

**Core principle:** verify the work against requirements, then judge its architectural quality independently. An author's report is a set of claims to check, not evidence that the design works.

Read [shared policies](../system-design-enter/references/policies.md), [operating method](../system-design-enter/references/methodology.md), **[review method](../system-design-enter/references/review-method.md)** and **[report contract](../system-design-enter/references/review-report.md)** before reviewing. Conceptual name: `system-design:review`; portable ID: `system-design-review`.

## Static boundary

Read/search files and relevant Git metadata. Do not run tests, application code, builds, containers, migrations, application API calls or database queries. If asked to execute them during review, explain the boundary and continue static analysis. Attribute existing test output to its source with limits; reading a test is not a passing run.

## Review sequence

1. **Prepare the brief.** Record requirements, decisions, scope, revision/local changes and unavailable evidence. Choose whole-project, focused change, design-only or re-review mode. Completion: assessed work and acceptance basis are explicit.
2. **Build the evidence map.** Start with a brief whole-project map, then trace the requested area/dependencies top-down: purpose ? participants/entities ? boundaries/relationships ? workflows/states ? layers/components ? contracts ? persistence ? transactions/concurrency ? integrations ? risks. Each main flow names authority, state owner and sources.
3. **Pass A ? Requirements compliance.** Check each scoped requirement for missing, extra or misunderstood behavior. Mark unavailable evidence separately. Label a defect mandated by the source design as design-mandated. Completion: each requirement has a supported status or explicit gap.
4. **Pass B ? Architectural quality.** Independently inspect boundaries, dependencies, contracts, transactions, repeated/concurrent intents, failures, compatibility and operational cost. Verify patterns through mechanics; preserve justified architecture. Read tests as behavioral intent only. Completion: concerns identify concrete mechanisms and consequences.
5. **Calibrate and challenge.** Check counter-evidence and author rationales. Separate structural defects, conditional risks and unknown runtime behavior. Use Critical/Important/Minor by impact; keep confidence separate. Include specific strengths. Each retained finding has location, invariant, consequence, basis and correction options/trade-offs.
6. **Self-review and report.** Check coverage, evidence, severity and claim limits. Give independent compliance/quality verdicts, unresolved information and explicitly declined-to-judge behaviors with reasons. Save/link the review in the shared review directory.

## Subject references and completion

Use [domain discovery](../system-design-enter/references/domain-discovery.md) for responsibility/vocabulary ambiguities; [relationships](../system-design-enter/references/context-relationships.md) for edges; [mechanisms/frameworks](../system-design-enter/references/relationship-mechanisms.md), [design patterns](../system-design-enter/references/design-patterns.md) and [architecture patterns](../system-design-enter/references/architecture-patterns.md) for pattern claims. Load `../system-design-microservices/SKILL.md` for service concerns once if not already active.

Without code assess requirements/design and state implementation absence. Re-review verdicts every prior finding and checks changes for named new risks; it does not repeat the entire audit. Red flags: unsupported all-clear, pattern-by-name, speculative Critical findings or a static risk called reproduced. Return to the evidence phase.

A review-only request stops here. For authorized review ? plan carry this artifact into `../system-design-plan/SKILL.md` without another permission question or routing loop. Correction options are not an implementation task list.
