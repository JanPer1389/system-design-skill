# Installation, updates and removal

Install the package separately for each host. The repository contains the skills plus native manifests, hooks and runtime adapters. It requires no MCP server or separately installed skill package. Python is for maintenance tools; Node is required for shell hooks and JavaScript adapters. Markdown-only discovery has no extra runtime requirement.

## Claude Code

```sh
claude plugin marketplace add JanPer1389/system-design-skill
claude plugin install system-design@system-design
```

For a temporary local session: `claude --plugin-dir ./system-design-skill`. Plugin-qualified invocation is `/system-design:system-design-review` and the four sibling IDs. Update through `claude plugin marketplace update system-design`, then `claude plugin update system-design@system-design`. Remove through `claude plugin uninstall system-design@system-design`, then `claude plugin marketplace remove system-design` if this source is no longer needed.

## Codex CLI and desktop

On a CLI supporting plugin management:

```sh
codex plugin marketplace add JanPer1389/system-design-skill
codex plugin add system-design@system-design
```

Use `$system-design-review`, `$system-design-plan` or the other discovered skill IDs. The Codex manifest uses native skill discovery and disables fallback loading of another host's hook configuration. Refresh a Git marketplace with `codex plugin marketplace upgrade system-design`, then reinstall/refresh the plugin and start a new session. Removal: `codex plugin remove system-design@system-design`, then `codex plugin marketplace remove system-design`.

Supported desktop clients can use the registered marketplace through their Plugins UI. Desktop UI installation and model behavior have not been verified by this package's local checks. Check your installed CLI's `--help` when commands differ by version.

## Gemini CLI

```sh
gemini extensions install https://github.com/JanPer1389/system-design-skill
gemini extensions update system-design
gemini extensions uninstall system-design
```

The declared `GEMINI.md` imports the common policies and host mapping. Restart sessions after changes.

## Pi

```sh
pi install git:github.com/JanPer1389/system-design-skill
```

Temporary local use: `pi -e ./system-design-skill`. Package resources are declared in `package.json`; the context extension restores the shared policies for transient provider requests. Update/remove the same package source with Pi's package manager, preserving its original project/user scope. An example removal is `pi remove git:github.com/JanPer1389/system-design-skill`.

## OpenCode

V1 configuration uses `plugin`; V2 uses `plugins` and requires the adapter contract available from V2 2.0.4:

```json
{"plugin":["system-design@git+https://github.com/JanPer1389/system-design-skill.git"]}
```

For V2 use the same entry under `plugins`. For local V2 registration use the package directory containing `index.js`, not a direct JavaScript-file path. Restart after updates; remove only this package's registration to uninstall. Actual host loading is unverified; confirm the configuration contract for your installed version. Adapter tests cover both API shapes, not the host's package manager/cache.

## Other native installers

- **Kimi Code:** `/plugins install https://github.com/JanPer1389/system-design-skill`, then `/reload` or `/new`. Update/remove through its plugin manager. Local installations are copied, so changing the original source requires reinstalling.
- **Copilot CLI:** `copilot plugin install https://github.com/JanPer1389/system-design-skill`; update with `copilot plugin update system-design`, remove with `copilot plugin uninstall system-design`.
- **Factory Droid:** `droid plugin marketplace add https://github.com/JanPer1389/system-design-skill`, then `droid plugin install system-design@system-design`. Use its manager for update/removal.
- **Qwen Code:** `qwen extensions install https://github.com/JanPer1389/system-design-skill` and select the package if prompted. Use its extensions manager for updates/removal.
- **Antigravity:** `agy plugin install https://github.com/JanPer1389/system-design-skill`; manage updates/removal through its native plugin tools.
- **Devin CLI:** `devin plugins install JanPer1389/system-design-skill`; check its plugin manager for update/removal commands in your version.
- **Hermes:** `hermes plugins install JanPer1389/system-design-skill --enable`; manage through its plugin manager. Very long compacted sessions may need a fresh session if the first-turn context is discarded.
- **Muse:** from a local checkout, `muse plugins install ./system-design-skill`, then `muse plugins approve system-design`; manage update/removal through its native plugin manager.
- **Cursor:** import the checkout from disk in Customize where local imports are allowed, or use the host's local plugin directory. Reload after updates; remove that registration to uninstall.

These additional integrations are implemented but not verified on actual installed hosts. Their availability is not a marketplace-publication claim. See [compatibility](compatibility.md).

## Portable local source and archive

From a checkout:

```sh
python scripts/package.py install --target ../system-design-local
python scripts/package.py pack --output ../system-design.zip
```

`install` prepares a source directory with `plugins/system-design/` and outer marketplace manifests; it does not install into an agent profile. Point a native marketplace installer at that prepared directory. Update it by repeating the same command. After removing host registrations, remove only its unchanged managed files with `python scripts/package.py remove --target ../system-design-local`.

The local-source manager preserves unowned files and refuses changed managed files, collisions, linked paths and traversal. Use one writer at a time. Process I/O failures are rolled back; power-loss/kill recovery is not a transaction guarantee. Archives contain the complete package and may be extracted elsewhere before validation.

To install skills directly without a plugin loader, place all five `skills/system-design-*` folders together in the agent's supported skills directory. Relative shared-reference paths require those sibling folders. Direct skill installs have no automatic startup hook.
