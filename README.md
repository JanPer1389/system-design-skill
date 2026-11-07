# System Design

Standalone, cross-agent skills for requirements discovery, domain modeling, architecture reviews, and detailed implementation planning.

## Skills

| Skill ID | Use it to |
| --- | --- |
| `system-design-enter` | Route an architecture request according to its outcome and available evidence. |
| `system-design-brainstorm` | Agree goals, entities, relationships, boundaries and scenarios through independent question rounds. |
| `system-design-review` | Review requirements and architectural quality in separate passes, with evidence, calibrated findings and explicit assessments. |
| `system-design-plan` | Produce an implementation handoff with exact file responsibilities, interfaces, tasks, TDD instructions and acceptance checks. |
| `system-design-microservices` | Evaluate service boundaries, ownership, consistency and failure recovery as a review/planning specialization. |

The skills ask questions, inspect code and design, and write architecture documents. They do not implement application changes or run the inspected application's tests, builds, services, migrations or database queries.

## Install

```sh
git clone https://github.com/JanPer1389/system-design-skill.git
```

Install **all five folders inside `skills/` together** in your agent's supported skills directory. Keep them as siblings: shared instructions live under `system-design-enter/references/`, and the other skills use relative links to that directory. Use your agent's documented skills installation mechanism and restart or reload its skill discovery as needed.

The agent needs skill loading or file reading, plus a way to discuss questions. A file writer is needed to save documents; without it, the skill returns the document in chat and states it was not saved. The instructions are self-contained and require no other skills. Automatic discovery and exact invocation syntax depend on the host; cross-host model behavior is not certified.

## Use

Ask your agent to use a skill by its ID. For example:

```text
Use system-design-brainstorm to explore the domain and boundaries of this application.
Use system-design-review to assess booking confirmation and its dependencies.
Use system-design-plan to prepare a detailed implementation handoff.
```

On hosts supporting Codex-style invocation, use `$system-design-review` and its siblings. On other hosts, use the discovered skill identifier or load its `SKILL.md`. Conceptual names such as `system-design:review` describe the operation; they are not universal command aliases.

A plan request includes the necessary static review when architectural decisions or code-grounded understanding are missing. Sufficient current evidence is reused. Brainstorm uses numbered independent question rounds and confirms the consolidated design before requested planning. Stopping questions leaves unresolved decisions explicit.

Architecture documents follow the user's language and belong under:

```text
docs/architecture/system-design/
├── review/
├── design/
└── plan/
```

## Method and references

Start from the smallest sufficient solution, usually a modular monolith for a server. Preserve justified existing architecture. Establish domain ownership and invariants before choosing patterns, frameworks or deployment boundaries. Separate code evidence, user decisions, agent conclusions, proposals and unknowns. Static inspection does not establish runtime correctness.

The [reference index](skills/system-design-enter/references/reference-index.md) leads to focused procedures for:

- [Domain discovery](skills/system-design-enter/references/domain-discovery.md).
- [Entity, context and dependency relationships](skills/system-design-enter/references/context-relationships.md).
- [Relationship mechanisms and framework facilities](skills/system-design-enter/references/relationship-mechanisms.md).
- [Design patterns](skills/system-design-enter/references/design-patterns.md).
- [Architecture patterns](skills/system-design-enter/references/architecture-patterns.md).
- [Review methodology](skills/system-design-enter/references/review-method.md), [question rounds](skills/system-design-enter/references/question-rounds.md), and [planning methodology](skills/system-design-enter/references/planning-method.md).

All skills follow one [shared policy source](skills/system-design-enter/references/policies.md). Reusable project examples use fictional names.

## Versioning and releases

The current release is recorded in [VERSION](VERSION). All five skills carry the same `metadata.version` in their frontmatter. The tracked locations are declared in [.version-bump.json](.version-bump.json); release history is kept in [RELEASE-NOTES.md](RELEASE-NOTES.md).

Maintainers can run the following commands from any directory with Python 3.10+ and no additional libraries:

```sh
python scripts/bump-version.py --check
python scripts/bump-version.py --audit
python scripts/bump-version.py 0.3.0
```

Use an absolute script path when running outside the repository. `--check` detects invalid, missing or inconsistent versions. `--audit` also finds undeclared references to the current version, excluding historical release notes. A version update validates every declared target and audits the old version before writing; it changes only version values and preserves skill bodies. Repeating the same update is safe. Use one version writer at a time; an interrupted process may require restoring consistency before retrying.

Follow `MAJOR.MINOR.PATCH`: major for incompatible changes to the published skill interface or workflow contract, minor for backward-compatible capabilities, and patch for compatible corrections or maintenance. Prerelease/build suffixes are supported. The command sets the exact requested version; it does not calculate increments or enforce chronological ordering.

For a release, update the version, add release notes, run both checks, then commit and tag the reviewed change as `v<version>`. Push the commit and that specific tag through your normal Git workflow. The script does not create commits, tags or releases automatically, and installed skills never invoke it as part of an architecture review.

## License

[MIT](LICENSE). Required third-party license notices are preserved in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
