# Brainstorm method: investigate, branch, decide, confirm

**Core principle:** the user supplies desired behavior and constraints; the agent investigates facts and proposes the architecture that follows. A technical pattern questionnaire is not domain discovery.

## 1. Investigate before the first round

Read the brief, settled conversation decisions, repository instructions and relevant code/design. Separate known facts, user decisions, agent proposals and unknowns. Identify whether this is one coherent project or genuinely independent initiatives. Use [domain discovery](domain-discovery.md) to find goals, participants, entities, language, relationships and boundaries. Do not ask a question answered by the sources.

Completion: a short known/unknown model with the highest-impact open branches. Do not restate the whole brief to prove you read it.

## 2. Build a dependency-aware question frontier

For each candidate question note what answer it needs first and what decision it would change. Ask only currently independent questions with settled prerequisites. Number them across rounds. Include a recommendation in user terms and a concise reason; do not make the recommended option smuggle in a technical choice the user need not make.

Example for fictional HarborDesk:

1. Who may confirm a booking? Recommendation: let staff confirm while members request, because the brief assigns capacity decisions to staff.
2. What should users see while confirmation is pending? Recommendation: an explicit pending state, so a request is not mistaken for an allocated room.

These can be independent if the brief already defines participants. A dependent question about self-service cancellation of an automatically confirmed booking must wait until automatic confirmation is chosen. "Should we use Saga or CQRS?" is not an appropriate business question.

Use the available question UI or chat. Then **wait**. Do not answer the round yourself because the next design step is convenient. Completion: answers are recorded with authorship; dependent branches can be reconsidered.

## 3. Recompute after each round

Close settled branches, identify contradictions and update the frontier. Reflect back consequential behavior briefly so the user can correct it. A new answer can invalidate a prior proposal; show the change rather than silently revising an agreed decision. Avoid reopening a settled choice unless new evidence creates a specific conflict.

Cover only relevant upper-level territory: goal/success, participants/authority, entities/lifecycles, relationships/boundaries, necessary functionality, important scenarios/states/failures, scope/exclusions and constraints. End questioning when these are sufficiently understood for the requested design, not when every imaginable topic has a question.

## 4. Compare architectural approaches

Once the relevant behavior is understood, present the credible ways to realize it. Ground each in requirements and the actual project. Explain what the user gains and pays: consistency, operational effort, migration and ability to change. Recommend the smallest sufficient option. If only one option is defensible, explain the constraints that rule out others; do not invent alternatives for symmetry.

Use [relationships](context-relationships.md), [mechanisms](relationship-mechanisms.md) and [architecture patterns](architecture-patterns.md) internally. The user approves consequential behavior/boundaries, not the name of a pattern. Record a delegated technical choice as an agent decision, not a user-authored one.

## 5. Consolidate and perform the builder check

Write the design with intent/why, goals/non-goals, actors, concepts/relationships, boundaries, scenarios/states, constraints, approaches/trade-offs, decisions/authorship and unresolved branches. Scale detail to the project; a small design can be short if it settles the same relevant questions.

Read it as an engineer who has the document and sources but not this conversation:

- What decision would I still have to guess that could change what gets built?
- Is the answer already in sources/conversation and merely missing from the design?
- Can I reasonably settle it within the delegated technical choices?
- Does it require the user's product/business decision?

Fill answers already available; settle minor delegated details and label them; bring only material user-owned gaps in an independent round. This is a self-review, not an automatic subagent dispatch or paid evaluation. Completion: a builder can prepare a plan without inventing the desired behavior.

## 6. Confirmation and early stop

Present/link the consolidated design and ask for confirmation before requested planning. Agreement on isolated answers is not confirmation of a document the user has not seen. After confirmation, follow the shared review gate before plan; do not repeat sufficient current inspection.

If the user stops, stop the questions and save a draft with unresolved branches and their consequences. Stopping questions does not approve them. If planning was also requested, present the consolidated draft for confirmation and do not proceed on unspecified material decisions. If the user explicitly delegates them, document that delegation and your choices before seeking the required design confirmation.

## Red flags

Asking facts already in code; mixing dependent questions in a round; making the user choose a framework/pattern instead of behavior; repeating settled decisions; treating silence/early stop as approval; writing a detailed plan before the design confirmation required by this discussion.

On any of these, return to the last settled decision frontier. Do not restart all questions or erase prior answers.
