# Host compatibility

Version requirements are unknown unless stated. Native installation tests, mock contracts and model behavior are different evidence levels. No integration requires an MCP bridge.

| Host | Discovery / bootstrap | Runtime | Verification / limitation |
| --- | --- | --- | --- |
| Claude Code | Root skills; SessionStart hook with nested additional context | Node on PATH for the hook | Isolated native install/reinstall/remove and strict manifests checked on CLI 2.1.233; model behavior unverified |
| Codex CLI | Manifest skills; native discovery; empty hooks suppress fallback hook loading | No extra runtime for skill discovery | Isolated native lifecycle checked on CLI 0.164.0-alpha.11.1; model behavior unverified |
| Codex desktop | Native plugin UI/discovery | Host | Implemented; actual UI unverified |
| Cursor | Manifest skills and sessionStart context hook | Node | Hook JSON contract checked; native install unverified; local imports may be restricted |
| Gemini CLI | Extension skills; GEMINI.md imports | Host | Imports/paths checked; native install/context expansion unverified |
| Pi | package.json skills plus transient context extension | Host JS/TS loader | Context reinjection, deduplication and summary preservation checked with mock host; native host unverified |
| OpenCode V1 | Config skills.paths and messages transform | Host Node/Bun | Mock discovery/bootstrap checked for V1 contract; native host unverified |
| OpenCode V2 | Native skill.transform; context/compaction/generate hooks | V2 2.0.4+ contract; host runtime | Three-hook mock contract checked; native host unverified |
| Kimi Code | sessionStart.skill plus skillInstructions | Host | Manifest/paths checked; native host unverified |
| Antigravity | Manifest and native skill index | Host | Implemented; native host unverified; eager bootstrap is not guaranteed |
| Devin CLI | Metadata manifest and root skills | Host | Implemented; native host unverified |
| Copilot CLI | Compatible manifest and top-level hook context | Node | Hook contract checked; native installation unverified; context output requires the host environment marker |
| Factory Droid | Compatible native plugin layout | Node for hook | Implemented; actual import/environment behavior unverified |
| Qwen Code | Compatible extension/plugin importer | Node if hooks are imported | Implemented; actual imported payload/bootstrapping unverified |
| Hermes | register_skill(Path, description); first-turn pre_llm_call | Host Python | Mock registration/context checked; native host unverified; first-turn bootstrap may be lost after compaction |
| Muse | Explicit native skill capabilities and SessionStart command | Node | Manifest/path and hook JSON checked; native host unverified; hook approval may be required |
| Grok Build CLI | No validated native integration | Unknown | Unsupported; generic file-reading use is not a verified native installation |

## Actions and boundaries

The [shared host mapping](../skills/system-design-enter/references/host-tools.md) maps loading, file reading/search, questions and document writing. Actual exposed tool names take precedence. Unsupported essential capabilities are reported rather than replaced with invented tools.

Every integration uses the same shared policies and five skill bodies. Native startup adapters load policies from the installed package. Skills also link to those policies for direct invocation. Python/Node validators do not establish that a model will always select or obey a skill. The [behavior protocol](../tests/behavioral-protocol.md) and raw fixtures remain available for separately authorized model evaluation.

Updates and removals use the host's own manager. Git-backed installers may cache a resolved revision; refresh/reinstall if restarting does not pick up the changed source. Do not delete a user's global configuration or unrelated plugins to clear a cache.
