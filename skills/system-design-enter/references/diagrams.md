# Architecture diagrams as evidence-bearing documents

The shared policies define when diagrams are required. Default to fenced `mermaid` blocks inside the user's Markdown artifact, with labels and explanations in the user's language. No image service, MCP connection or renderer is required. Do not install tooling or run application commands to produce a diagram.

## Select the view

- System/context flowchart: participants, domain/module responsibilities, external systems and owned stores. Group components in one process when deployment separation is not established.
- Sequence diagram: an important interaction, authority, transaction boundary, response and relevant failure/retry path. Split separate scenarios rather than inventing a giant flow.
- State diagram: lifecycle transitions, who can cause them and rejected/terminal states.
- Entity diagram: meaningful data relationships; distinguish ownership and cardinality from transport and runtime calls.
- Migration flow: existing, transitional and target arrangements when coexistence matters.

Use the fewest views that explain the decision. A prompt-only design needs a preliminary overview once sufficient facts exist, not every possible diagram. A substantial plan often needs a target overview plus a sequence for its hardest invariant.

## Construct and check

1. Name the scope and status: current/inspected, proposed or preliminary. Use separate current and target diagrams when mixing them would imply that a proposal already exists.
2. Trace current edges/nodes to inspected sources. Put references in adjacent prose or a compact evidence table. Label inferred/unknown edges explicitly; dashed lines alone have no universal meaning, so include a legend. For prompt-only models state that implementation is absent and list material assumptions.
3. Name each important edge's command/query/event or data purpose and each store's owner. Do not imply separate services merely by drawing separate boxes, or atomic distributed writes merely by drawing an arrow.
4. Keep identifiers simple, quote human-readable labels and prefer common flowchart/sequence syntax. Check node references, participant names, direction, ownership and consistency with prose/contracts/tasks. Avoid renderer-specific features unless verified available.
5. If an existing non-application renderer/parser is available and its use is permitted, validate the document without importing/running the application or installing dependencies. Otherwise say the Mermaid source was checked by inspection and rendering was not verified; do not claim a successful render. Include a brief textual explanation so the artifact remains useful without rendering.

## Handoff and revisions

Place diagrams next to the decision/workflow they explain. Keep source in the Markdown document; separate `.mmd` files only when useful for a large requested artifact, without creating a second inconsistent authority. Update diagrams when decisions change and explain the change. Carry forward or link an unchanged diagram instead of redrawing it in each message. If a requested view cannot be grounded in available facts, show the supported portion with explicit unknowns or explain the missing basis; never fabricate the missing infrastructure.
