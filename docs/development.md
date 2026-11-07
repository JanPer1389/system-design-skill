# Package maintenance

Use Python 3.10+ and Node 22.18+. The package scripts use only standard libraries. The optional pre-commit configuration runs package validation and version audit through the existing Python environment; installing pre-commit is not required to use the skills.

## Validate

```sh
python scripts/bump-version.py --audit
python scripts/validate.py
python -m unittest discover -v -s tests -p 'test_*.py'
node --test tests/integrations.test.mjs
```

Tests cover version synchronization, manifest paths, packaging, installation/update/removal ownership, relocation, bootstrap shapes, native registration and transient context handling. They do not execute the fixture application or make model calls. A Windows account without symlink privileges skips the OS symlink test explicitly. GitHub Actions runs the offline suite on Linux and Windows when workflow execution is available.

`tests/native-host-smoke.ps1` additionally checks local Codex/Claude installation with new disposable profiles. Pass a local marketplace source and a fresh profiles directory. The script restores environment variables and never copies credentials or prompts a model. See [verification](verification.md).

## Version and release

`VERSION`, all skill metadata and every versioned host manifest are declared in `.version-bump.json`. JSON dotted fields can address marketplace array entries; YAML support is limited to a single flat scalar field, and skill support addresses quoted `metadata.version` in frontmatter.

```sh
python scripts/bump-version.py --check
python scripts/bump-version.py --audit
python scripts/bump-version.py NEW_VERSION
```

Replace `NEW_VERSION` with the target semantic version. The command validates all targets and audits the old version before writing. It preserves surrounding content and rolls back an ordinary write failure. Use one writer at a time; interruptions/power loss are not transactional. It sets the exact requested semantic version and does not infer increments or prevent a deliberate downgrade. Follow MAJOR.MINOR.PATCH according to the published interface/workflow contract, add release notes, and check the resulting diff before committing/tagging through the authorized Git workflow.

## Package inventory

`package-files.json` is the explicit file list for a clean release. Update it when adding/removing maintained files. Exclude scratch directories, credentials, generated archives, bytecode, external reference repositories and private project specifications. The structural validator rejects incomplete or stale inventories.

## Contribute

Read [AGENTS.md](../AGENTS.md). Keep changes scoped, preserve shared-policy authority and report validation honestly. Submit evidence for claimed host support. Model evaluation can incur costs and needs separate authorization; scenario fixtures are not passing results.
