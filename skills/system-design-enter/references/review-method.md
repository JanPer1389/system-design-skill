# Architectural review method

**Core principle:** compare the work with its requirements, then judge the actual design on its merits. These are separate judgments. An implementation can match a flawed design, or use a sound mechanism while omitting a required scenario. Author reports and reassuring names are claims to verify.

Always apply the shared static-review boundary. Read code/design/tests/configuration and relevant Git metadata; do not run tests, application modules, builds, containers, database queries or application external calls. This is an architectural assessment, not runtime certification.

## Phase 1 — Prepare a precise review brief

Capture requested outcome/scope, binding requirements, design decisions, sources, revision and local changes when available. Select one mode:

- **Whole project:** brief map of purpose, participants, domain responsibilities and important flows; then prioritize affected or highest-risk paths.
- **Focused area/change:** brief system context, target contract/change and immediate dependencies. Inspect additional files for a named risk; explain why the scope expanded.
- **Requirements/design without implementation:** assess intended behavior, boundaries and contradictions. Say implementation is absent; implementation compliance is not assessable.
- **Re-review:** previous finding IDs, reviewed revision and fix scope. Use the focused re-review procedure below rather than repeat the entire audit.

Do not manufacture base/head SHAs for a non-Git project or require a branch/worktree. Do not silently discard claims whose evidence is missing: list them as unverified and identify the missing source. Completion: another reviewer could tell exactly what is being judged against what.

## Phase 2 — Build the current model from sources

Work top-down: purpose → participants/entities → boundaries/relationships → workflows/states → layers/components → contracts → persistence → transactions/concurrency → integrations → risks.

1. Inventory entry points, key modules, state owners and external parties from files.
2. Use [domain discovery](domain-discovery.md) for responsibility and vocabulary ambiguities; record current versus proposed boundaries separately.
3. Use [context relationships](context-relationships.md) for important edges; distinguish domain influence, code dependency and runtime calls.
4. Trace each scoped important workflow from request to decision, write/integration and result, including a repeated request and a failure path where relevant.
5. Verify claimed patterns through participants, control flow and persistence/delivery mechanics using [design](design-patterns.md), [architecture](architecture-patterns.md) and [relationship mechanisms](relationship-mechanisms.md).

Every major structural claim needs a file/symbol/location or a design source. A dependency in package metadata establishes availability, not use. Tests as text establish intended coverage, not successful execution. Completion: a concise architecture/flow map with evidence and explicit gaps, not an inventory of filenames alone.

## Phase 3 — Pass A: requirements and decision compliance

Compare each scoped requirement with the inspected mechanism. Classify:

- **Satisfied by inspected design:** cite the matching mechanism and limits.
- **Missing:** a required behavior or invariant lacks implementation/design support in the inspected scope.
- **Extra:** a capability or infrastructure cost has no demonstrated requirement; distinguish harmless optional code from consequential scope expansion.
- **Misunderstood:** the implementation handles a superficially similar case while missing the intended behavior.
- **Cannot verify:** the required source or runtime evidence is unavailable; state what would resolve it.

Check departures from the approved design separately. A justified improvement is not automatically a defect; a defect mandated by the design is still a finding labeled **design-mandated**. Do not let the author grade their own rationale.

Requirements do not enumerate every input. Consider ordinary cases implied by the affected invariant (duplicate delivery, missing authorization, concurrent ownership) and label the reasoning. Do not invent product policy where several materially different behaviors are valid: mark the decision open. Completion: all scoped requirements have a supported status, and product ambiguity is separate from implementation omission.

## Phase 4 — Pass B: architectural quality

Evaluate the actual design independently of Pass A:

| Area | Investigation |
| --- | --- |
| Boundaries | Cohesive domain responsibilities, coherent language, public capabilities, protected internals |
| Dependencies | Direction/cycles, actual coupling, callers affected by contract changes |
| State and consistency | Authority, lifecycle, constraints, transaction/session scope, concurrent attempts |
| Repeats and failures | Same versus new intent, atomic deduplication/effect, timeout ambiguity, recovery owner |
| Contracts | Inputs/outputs/errors, compatibility, translation of external meanings, authorization boundaries |
| Operational fit | Stated scale/isolation/release needs and the cost of the proposed topology |
| Verification design | Tests as text cover real behaviors/invariants; missing meaningful cases and external assumptions |
| Evolution | Migration/coexistence, data ownership changes, rollback/recovery limits |

Preserve good mechanisms and cite their evidence under strengths. Do not recommend layers, microservices or a framework merely because they appear in a reference. Completion: every significant quality concern has a concrete location, consequence and basis, not generic advice.

## Phase 5 — Calibrate findings and challenge them

Before keeping a finding, ask: what requirement/invariant is at stake, which source proves the mechanism, what counter-evidence was checked, and how certain is the consequence? Distinguish a confirmed structural defect, a conditional static risk and unknown runtime behavior.

| Severity | Apply when | Do not use for |
| --- | --- | --- |
| Critical | Inspected evidence establishes a material path to serious loss/security exposure or invalidates a fundamental stated invariant; explain the conditions | Speculative scale, a pattern preference or absence of a fashionable tool |
| Important | A concrete required behavior/boundary/consistency or migration problem must be resolved before relying on this design for the scoped goal | General desire for more coverage or cosmetic structure |
| Minor | Improvement with limited present impact; documentation/polish or nonblocking simplification | Hiding a missing requirement or serious uncertainty |

Keep confidence separate from severity. If an unknown could conceal serious impact, state "material unknown preventing assessment" and what is missing; do not present an unproven defect as Critical. Acknowledge an author's counter-evidence and revise/discard the finding if it resolves the concern.

## Phase 6 — Report, self-review and stop

Use [the report contract](review-report.md). Give separate compliance and quality assessments, strengths, calibrated findings, correction options/trade-offs, unresolved information and behaviors explicitly declined to judge. Explain why each excluded item is out of scope or unverifiable. An empty declined list means none were set aside, not that the field was skipped.

Self-review coverage of the brief, traceability of findings, consistency of pattern claims, severity and claim limits. A review-only request ends here. If this is the required review for an authorized plan, carry the review forward without another permission question. Corrective options explain alternatives; the ordered implementation task list belongs to plan.

## Focused re-review

Read prior findings and the changed sources once. Verdict every prior finding: **Addressed / Still open / Cannot verify**, with current evidence. Inspect affected dependencies for named new risks introduced by the change. Record newly noticed unrelated issues separately; do not reopen the whole audit or extend the review loop without grounds. "Attempted" is not "Addressed": the specific structural concern must be resolved in the inspected design. Runtime fix success remains unverified.

## Red flags

- Accepting an implementation report without checking sources.
- Replacing evidence with the presence of a class/package name.
- Treating a preferred architecture as a requirement.
- Downgrading a serious defect because the plan mandated it.
- Claiming a static risk was reproduced, or test text proves a passing run.

On a red flag, return to the relevant phase and narrow the claim. Do not start application execution to rescue an unsupported assertion.
