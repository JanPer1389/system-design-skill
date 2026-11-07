# Repository guidance

This repository is the installable System Design package. Keep skill instructions, native integrations, tests and documentation together. Do not add private project specifications, authoring checkouts, credentials, scratch directories or generated archives.

## Scope

Installed skills discuss requirements, inspect architecture statically and write designs/reviews/plans. Preserve those boundaries. Developing this package permits running its own validators and infrastructure tests; the installed review restriction does not prohibit that maintenance work.

Read affected skills and shared references before changing behavior. Keep shared authority in `skills/system-design-enter/references/policies.md`. Preserve relative paths and fictional reusable examples. Do not change skills merely to accommodate a host's tool names; update its adapter/mapping instead.

## Integration and release changes

- Declare every release-version location in `.version-bump.json`; keep `VERSION`, skills and host manifests synchronized.
- Root marketplaces load this repository as a plugin. `scripts/package.py install` prepares a separate local source and rewrites only the outer marketplace paths for that layout.
- Native integrations must resolve package assets from their installed location and preserve existing host settings.
- Keep third-party license notices. Do not claim a native host or model behavior was verified when only a schema/mock contract was tested.
- Use a compatible version bump and update `RELEASE-NOTES.md`. Commits, tags and publication require the user's requested scope; scripts do not perform them automatically.

## Checks

From the repository root, with Python 3.10+ and Node 22.18+:

```sh
python scripts/bump-version.py --audit
python scripts/validate.py
python -m unittest discover -s tests -p 'test_*.py'
node --test --test-isolation=none tests/integrations.test.mjs
```

Model evaluations may incur costs and require separate authorization. Use disposable profiles for native install smoke checks; never copy credentials from the maintainer's live profile. Inspect Git state and preserve unrelated work.
