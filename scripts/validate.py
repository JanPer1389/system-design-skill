"""Offline structural validator; does not claim model compliance or host certification."""
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
IDS = {"system-design-" + mode for mode in ("enter", "brainstorm", "review", "plan", "microservices")}


def validate(root=ROOT):
    errors = []
    def check(condition, message):
        if not condition:
            errors.append(message)
    inventory = json.loads((root / "package-files.json").read_text(encoding="utf-8"))
    check(len(inventory) == len(set(inventory)), "duplicate inventory entry")
    actual = {p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file()
              and not any(part in {"__pycache__", ".git"} for part in p.relative_to(root).parts)}
    check(set(inventory) == actual, f"inventory mismatch: {sorted(set(inventory) ^ actual)}")
    package = json.loads((root / "package.json").read_text(encoding="utf-8"))
    skills = list((root / "skills").glob("*/SKILL.md"))
    check({s.parent.name for s in skills} == IDS, "expected exactly five skill IDs")
    for file in skills:
        text = file.read_text(encoding="utf-8")
        match = re.match(r"\A---\nname: ([a-z0-9]+(?:-[a-z0-9]+)*)\ndescription: ([^\n]+)\n(?:metadata:\n  version: \"[^\n]+\"\n)?---\n", text)
        check(bool(match), f"invalid frontmatter: {file.relative_to(root)}")
        if match:
            check(match[1] == file.parent.name and len(match[1]) <= 64, f"invalid skill ID: {file}")
            check(1 <= len(match[2]) <= 1024 and not any(c in match[2] for c in "<>"), f"invalid description: {file}")
        check("references/policies.md" in text, f"shared policies not linked: {file}")
    for name in inventory:
        file = root / name
        check(not file.is_symlink(), f"symlink in package: {name}")
        if file.suffix not in {".md", ".json", ".yaml", ".py", ".js", ".cjs", ".ts"} and file.name != "LICENSE":
            continue
        text = file.read_text(encoding="utf-8")
        check(not re.search(r"(?i)(?<![\w/])(?:[a-z]:[/\\]|[/]Users[/]|[/]home[/][^/]+[/])", text), f"local absolute path: {name}")
        if file.suffix == ".json":
            try:
                obj = json.loads(text)
                if file.name in {"plugin.json", "package.json", "gemini-extension.json"}:
                    check(obj.get("version") == package["version"], f"version mismatch: {name}")
                    check(obj.get("name") == "system-design", f"identity mismatch: {name}")
            except json.JSONDecodeError:
                errors.append(f"invalid JSON: {name}")
        if file.suffix == ".md":
            for link in re.findall(r"\]\(([^)]+)\)", text):
                if "://" in link or link.startswith("#"):
                    continue
                link = link.split("#")[0]
                target = (file.parent / link).resolve()
                check(target.is_relative_to(root.resolve()) and target.exists(), f"broken/escaping link in {name}: {link}")
    # Validate manifest paths, rather than just accepting syntactically valid JSON.
    paths = [package["main"], *package["pi"]["extensions"], *package["pi"]["skills"]]
    for host in ("codex", "cursor", "kimi"):
        manifest = json.loads((root / f".{host}-plugin/plugin.json").read_text(encoding="utf-8"))
        paths.append(manifest["skills"])
        if isinstance(manifest.get("hooks"), str):
            paths.append(manifest["hooks"])
    muse = json.loads((root / ".muse-plugin/plugin.json").read_text(encoding="utf-8"))
    check({s["id"] for s in muse["capabilities"]["skills"]} == IDS, "Muse IDs mismatch")
    paths.extend(s["path"] for s in muse["capabilities"]["skills"])
    paths.append(json.loads((root / "gemini-extension.json").read_text(encoding="utf-8"))["contextFileName"])
    for name in paths:
        target = (root / name).resolve()
        check(target.is_relative_to(root.resolve()) and target.exists(), f"missing/escaping manifest path: {name}")
    for line in (root / "GEMINI.md").read_text(encoding="utf-8").splitlines():
        if line.startswith("@"):
            check((root / line[1:]).is_file(), f"broken Gemini import: {line}")
    codex = json.loads((root / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
    check(codex.get("hooks") == {}, "Codex must suppress Claude hook auto-discovery")
    scenarios = json.loads((root / "tests/scenarios.json").read_text(encoding="utf-8"))
    check(len(scenarios) >= 12, "insufficient behavioral scenarios")
    for case in scenarios:
        check(all(case.get(key) for key in ("id", "request", "context", "expected", "forbidden")), f"incomplete scenario: {case.get('id')}")
        for name in case.get("files", []):
            check((root / "tests/fixtures" / name).is_file(), f"missing scenario fixture: {name}")
    return errors


if __name__ == "__main__":
    try:
        failures = validate()
    except (OSError, ValueError, KeyError) as error:
        failures = [str(error)]
    for error in failures:
        print("FAIL:", error)
    print(f"Structural validation: {len(failures)} error(s); behavioral execution is separate")
    sys.exit(bool(failures))
