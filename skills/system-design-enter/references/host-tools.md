# Host action mapping

The actual exposed tool list is authoritative. Names below describe known contracts, not tools to invent. These actions do not expand shared-policy permissions. Use shell only for file reading/search and relevant read-only Git metadata, never for application execution in review. Write only the requested architecture artifacts.

| Action | Claude / compatible hosts | Codex | Gemini | OpenCode V1 / V2 | Pi | Kimi | Hermes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Load skill | native Skill with the discovered ID | native discovery, read installed SKILL.md if needed | native skill activation, or read installed file | native skill loader with its exposed parameters | read installed SKILL.md | Skill | skill_view, fallback read_file |
| Read/search | Read, Grep, Glob | available file tools or read-only shell | available read/search tools | read, grep, glob | read, optional grep/find/ls | Read, Grep, Glob | read_file and exposed search |
| Ask/wait | native question UI or chat | available question UI or chat | question UI or chat | exposed question UI or chat | chat | AskUserQuestion or chat | chat |
| Write artifact | Write/Edit | apply_patch or available file tool | available write tool | apply_patch / patch, write/edit | write/edit | Write/Edit | available write tool |

Cursor, Antigravity, Devin, Muse, Factory Droid, Qwen and Copilot use their actual native tools; sharing skill instructions does not prove identical tool signatures. Use file reading if a skill loader cannot resolve the portable ID. If the host cannot read files, disclose the missing capability and stop dependent work. If writing is unavailable, return the unsaved artifact in chat with its intended path. No mandatory subagent, todo, browser, MCP or application shell capability exists.

## Identifiers

| Conceptual name | Folder/frontmatter / skill ID |
| --- | --- |
| system-design:enter | system-design-enter |
| system-design:brainstorm | system-design-brainstorm |
| system-design:review | system-design-review |
| system-design:plan | system-design-plan |
| system-design:microservices | system-design-microservices |

Codex explicit syntax is `$system-design-enter` and its four siblings. Pi explicit syntax is `/skill:system-design-enter`. Other loaders use the discovered portable IDs and their actual invocation syntax. This repository distributes skills directly, so no plugin-qualified alias is assumed. Conceptual colon names are documentation labels, not promised aliases on every host. Sibling locations are `../../<portable-ID>/SKILL.md` from this references directory.
