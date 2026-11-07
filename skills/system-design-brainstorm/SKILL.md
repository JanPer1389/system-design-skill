---
name: system-design-brainstorm
description: Use when the user wants to explore or agree application goals, domain concepts, boundaries, essential scenarios and architectural choices through discussion.
metadata:
  version: "0.3.0"
---

# Brainstorm a system design

**Core principle:** investigate facts yourself; help the user settle consequential behavior; derive technical proposals from those decisions. Read [shared policies](../system-design-enter/references/policies.md), [operating method](../system-design-enter/references/methodology.md) and **[question-round method](../system-design-enter/references/question-rounds.md)**. Conceptual name: `system-design:brainstorm`; portable ID: `system-design-brainstorm`.

## Discussion sequence

1. **Look before asking.** Read supplied context, settled decisions, repository rules and relevant implementation/design. Separate facts, user decisions, proposals and open branches. Completion: questions add information the sources cannot provide.
2. **Model the problem.** Use [domain discovery](../system-design-enter/references/domain-discovery.md) for goals, participants/authority, entities/lifecycles, vocabulary, relationships and application boundaries. Cover necessary functionality, important workflows/states/failures and constraints at the relevant depth.
3. **Ask an independent round.** Select questions with settled prerequisites. Number them across rounds; include a recommendation and concise rationale in user terms. Defer dependent questions. Use the native question UI or chat, then **wait for answers**. Completion: the current frontier is settled before dependent choices are asked.
4. **Update and play back.** Record authorship, close answered branches and reflect consequential behavior briefly for correction. Recompute the next frontier. Do not repeat settled decisions or make the user choose patterns/frameworks.
5. **Compare approaches.** Present credible options grounded in agreed behavior and constraints. Explain gains, consistency/migration/operating costs and recommend the smallest sufficient choice. If only one is defensible, explain why. Record delegated technical choices as yours.
6. **Consolidate and perform the builder check.** Write intent, goals/non-goals, concepts/relationships, boundaries, scenarios/states, constraints, alternatives, decisions/authorship and open issues. Read as an engineer without the conversation: fill known answers, settle minor delegated details and ask materially consequential user-owned gaps. This is self-review, not automatic delegation.
7. **Confirm and finish.** Save/link the design in the shared directory. Present the consolidated design for confirmation before requested planning. Completion: relevant upper-level choices are understood and confirmed, or early stop is recorded honestly.

## Conditional detail

Use [context relationships](../system-design-enter/references/context-relationships.md) for interacting areas, [mechanisms](../system-design-enter/references/relationship-mechanisms.md) to derive communication/contracts and [architecture patterns](../system-design-enter/references/architecture-patterns.md) for alternatives. Consult [the fictional tree](../system-design-enter/references/project-tree.md) only for an adapted structure; it is not a scaffold.

## Gates and early stop

Answers settle only choices shown. Agreement with an idea is not confirmation of an unseen design. End when the relevant design is understood/agreed or the user stops, rather than pursuing checklist completeness. On early stop save a draft with unresolved choices and consequences; stopping does not approve them.

After confirmation load `../system-design-plan/SKILL.md` only if requested, following its review gate. Do not implement. Red flags: dependent questions in one round, technical quizzes, endless questions, proposals silently becoming user decisions. Correct the current branch rather than restart the discussion.
