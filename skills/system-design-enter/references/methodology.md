# Operating method: evidence before conclusions

**Core principle:** understand the intended behavior, inspect the actual mechanism, then make the smallest defensible architectural decision. A named role or a checklist of topics is not the method: each phase must produce an observable result that the next phase consumes.

## 1. Establish the brief

Identify the requested outcome, affected area, applicable repository rules, supplied requirements/design/review and evidence available now. Separate user decisions from an author's claims about what was built. Determine whether this is requirements discussion, review, planning or a specialization. State missing capabilities once and continue unaffected work. Completion: a scope statement plus sources and the question the artifact must answer.

For an existing project, create a short whole-project map before deep inspection. For a change, identify changed contracts and their immediate dependents. For a no-code idea, say that implementation is absent and examine the intended design instead. Scope controls depth; it does not excuse ignoring an immediately affected invariant.

## 2. Build a traceable model

Move from purpose through domains and interactions to components and persistence. Keep a compact working ledger:

| ID | Category | Statement | Basis | Consequence / status |
| --- | --- | --- | --- | --- |
| R1 | requirement | One confirmed holder per slot | user brief | must hold under concurrency |
| E1 | code evidence | confirmation writes status in a local transaction | inspected symbol/revision | does not yet establish slot exclusivity |
| H1 | agent hypothesis | concurrent confirmations may both succeed | E1; constraint evidence incomplete | inspect schema and callers |
| D1 | user decision | keep a single-process deployment | explicit user choice | preserve unless conflict is surfaced |
| P1 | proposal | enforce exclusivity at the authoritative write | R1, investigated evidence | compare viable mechanisms |

Use only relevant rows; do not turn every sentence into bookkeeping. Each material conclusion must resolve to a source, explicit user decision or labeled assumption. Completion: important workflows, owners and invariants can be explained without relying on a suggestive identifier.

## 3. Investigate before proposing

For a suspected problem, state the hypothesis and the evidence that would contradict it. Trace the entry, state owner, transaction, dependencies and result; inspect the smallest additional source needed. Compare with a working mechanism in the same project before introducing a new abstraction. Search further when a named risk requires it, not merely because more files exist.

Static investigation can establish a missing constraint in the inspected schema or a dependency violation. It cannot reproduce a race or certify a running service. If an essential source is unavailable, keep the hypothesis conditional. Completion: every proposed correction has an identified problem/invariant and an evidence basis; unsupported pattern labels are removed or marked unknown.

## 4. Decide proportionately

Compare the smallest sufficient option with credible alternatives. Record requirement, constraints, chosen mechanism, cost, rejected alternative and revisit trigger. Preserve established architecture where it satisfies requirements. If the provided design itself contradicts a requirement, label a design defect instead of treating plan authorship as proof of correctness.

Brainstorm obtains user decisions through independent question rounds and confirms the consolidated design. Outside brainstorm, settle defensible details autonomously and mark assumptions; ask only about a blocking material decision. The shared plan gate remains authoritative. Completion: the next phase can distinguish what is agreed, inferred, proposed and unresolved.

## 5. Produce and challenge the artifact

Use the selected operation's output contract. Then take a fresh pass from the recipient's perspective:

1. **Coverage:** map every scoped requirement to evidence, a decision or an explicit unresolved item.
2. **Consistency:** compare names, owners, interfaces and guarantees across the artifact.
3. **Failure behavior:** examine repeat intent, concurrency and partial failure for affected writes.
4. **Proportion:** remove infrastructure or full implementation bodies that the decision does not need.
5. **Claim check:** identify what proves each conclusion, read that evidence, limit the claim, then state it.

Fix supported omissions before handing over. Missing evidence produces a limitation, not a fabricated success. Save/link the document in the shared artifact directories; report an unsaved artifact honestly if no writer exists. Completion: a recipient can act on the artifact within its stated limits without reconstructing the author's conversation.

## Stop and correct course

| Temptation | Required correction |
| --- | --- |
| "The author says it is idempotent" | Trace identity, atomic effect and concurrent retry handling |
| "A library named Saga is installed" | Inspect compensation, persistence and recovery before naming the pattern |
| "The spec is silent, so ignore this case" | Derive the affected invariant; label inferred expectations and resolve material ambiguity |
| "A long report proves completeness" | Check scoped requirements and evidence coverage |
| "The plan commands look right, so they passed" | Keep them as unexecuted instructions |

These are anticipated failure checks, not a claim that a model evaluation observed them. Stop only the dependent work for a material unresolved decision or unavailable essential capability; continue useful analysis elsewhere. The installed package never starts application implementation.
