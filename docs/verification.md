# Verification scope

Local checks distinguish package correctness from host/model behavior. The current maintenance environment uses Windows, Python 3.14.3 and Node 24.19.0. Available native CLIs are Codex 0.164.0-alpha.11.1 and Claude Code 2.1.233.

## Checked locally

The instruction-update local run completed 27 Python tests with 26 passing and one explicit Windows symlink-privilege skip. All six Node integration-contract tests passed. The package structural validator checks the five skill identifiers/frontmatter, reference graph and manifests. The external authoring validator could not run in this maintenance environment because its PyYAML dependency is unavailable; it is not a package runtime dependency.

Earlier package revisions passed the external authoring schema validator, strict Claude plugin/marketplace validation and isolated Codex/Claude lifecycle checks for both repository-root and prepared local-source layouts. Those native lifecycle checks were not repeated for this instruction-only update.

- Skill metadata, shared references, manifest identities/versions/paths and complete package inventory.
- Version checks/audit and synchronized updates across text, skill, JSON and YAML fields, including invalid/missing targets and write rollback.
- Portable archive extraction, independent validation/installation, Unicode/spaced target paths and repeated installation/update/removal while preserving unrelated files.
- Host-specific hook outputs, missing-policy errors, OpenCode V1/V2 mock discovery/bootstrap, Pi context reinjection and Hermes registration.
- Isolated local Codex/Claude install, repeated install and removal; strict Claude manifest validation.

Run the commands in [development](development.md) to reproduce package checks. The Windows symlink test is skipped if the account lacks creation rights; that skip does not establish OS verification of symlink/junction rejection. Other hosts are described as implemented-but-unverified in [compatibility](compatibility.md).

## Not established

No paid model evaluation has been run. The behavioral scenarios have raw inputs and observable criteria but remain execution-unverified. Native installation success does not prove automatic skill activation or compliance by every model. Linux/macOS native host installation is not established by the local Windows run. CI results must be read from the actual workflow before being called passing.

## Native isolated smoke check

On PowerShell with both CLIs installed:

```powershell
python scripts/package.py install --target ../system-design-local
& ./tests/native-host-smoke.ps1 -SourceRoot ../system-design-local -ProfilesRoot ../system-design-disposable-profiles
```

ProfilesRoot must not already exist. Keep it separate from live settings and do not copy credentials. The script runs no model prompt. Remove the disposable directory only after inspecting its resolved path and preserving anything you deliberately added.

## Architecture-planning instruction update

The new stack-assessment, diagram and visible-plan instructions have static cross-reference/inventory checks and behavioral scenarios 22–26 with raw input. Their observable model behavior remains execution-unverified; no paid model evaluation was authorized. Existing native installation results above are historical infrastructure evidence, not a new host/model certification for these instructions. Mermaid rendering of the illustrative reference has not been verified; its labels and ownership have been inspected as source.
