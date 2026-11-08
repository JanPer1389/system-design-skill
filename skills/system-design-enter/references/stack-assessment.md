# Assess architecture and tooling independently

Use this method when a material choice affects the requested design, review or plan. Do not expand a focused review into an unrelated tool migration.

## Establish the decision, not a technology wishlist

1. Read manifests, dependency declarations/locks, CI configuration and relevant code as text. Record actual versions, runtime constraints, integrations and deployment/maintenance capacity; absence from inspected files does not prove absence elsewhere.
2. Separate binding user/external constraints, tentative suggestions, current implementation and agent recommendations. Translate technical uncertainty into the business fact needed; do not ask a nontechnical user to choose a framework.
3. Identify a concrete need: reproducible environments, supported runtime, compatibility, delivery effort, reliability, security maintenance, latency or operational cost. Check whether the existing mechanism already satisfies it.
4. Compare retaining/improving the current approach with credible replacements. Consider feature fit, ecosystem/support, deployment compatibility, lock/export behavior, CI/cache integration, team burden, migration and rollback. Choose the smallest sufficient option; retain the current tool when switching has no material benefit.
5. Verify changing product claims with official documentation or upstream repositories. Record links, relevant version/date and limits. Do not infer security from popularity, a lockfile or a product name. Without browsing, mark the relevant claims unverified and avoid pretending an exact version is current.
6. Record the agent recommendation, plain-language benefit, evidence, trade-offs, affected files/workflows, acceptance checks and revisit trigger. A recommendation is not an executed migration or user approval.

## Example: Python dependency management

Finding `requirements.txt` is a reason to inspect the workflow, not proof of insecurity. Read whether direct/transitive dependencies are pinned, how environments are reproduced, development groups separated, Python versions constrained and CI/container/deployment inputs generated. Check for existing compilation/constraint tooling before suggesting replacement.

If reproducibility or packaging needs justify it, evaluate a project declaration in `pyproject.toml` plus an appropriate resolver/lock workflow, including uv and Poetry where compatible. A declaration format, a tool and a lockfile are different things. Verify the candidate's actual lock/sync/export/support behavior in its official documentation; this reference does not assert current feature parity or universal superiority. Retaining a requirements-based deployment export can be appropriate. A transition plan owns runtime declarations, dependency groups, lock generation, CI commands, deployment compatibility, reproducibility checks and rollback; it does not blindly rename a file or run a tool during review.

## Apply by operation

- Enter: carry detected constraints and material stack questions to the requested operation; do not invent another approval gate.
- Brainstorm: ask about product/operating constraints and decide the technical approach; explain meaningful consequences and confirm the consolidated design.
- Review: report limitations with evidence and alternatives; distinguish defects from optional improvements. Do not write an unsolicited migration task list.
- Plan: establish a coherent target, then assign dependency/config/CI/migration changes and checks to exact tasks. They are future executor instructions.
- Microservices: assess transport, SDK, persistence and observability choices against ownership, consistency, failure behavior and operating capacity; a product does not justify a service boundary.
