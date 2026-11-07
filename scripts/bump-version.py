#!/usr/bin/env python3
"""Check, audit or update all declared release versions. Python standard library only."""
import argparse
import fnmatch
import json
import os
from pathlib import Path, PurePosixPath
import re
import sys
import time
import uuid

ROOT = Path(__file__).resolve().parents[1]
NUMBER = r"(?:0|[1-9][0-9]*)"
PRE = r"(?:0|[1-9][0-9]*|[0-9]*[A-Za-z-][0-9A-Za-z-]*)"
SEMVER = re.compile(rf"{NUMBER}\.{NUMBER}\.{NUMBER}(?:-{PRE}(?:\.{PRE})*)?(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?")


def valid_version(value):
    if not isinstance(value, str) or not SEMVER.fullmatch(value):
        raise ValueError(f"Invalid semantic version: {value!r}")
    return value


def safe_path(name):
    if not isinstance(name, str) or not name or PurePosixPath(name).is_absolute() or ".." in PurePosixPath(name).parts or "\\" in name or ":" in name:
        raise ValueError(f"Unsafe declared path: {name!r}")
    path = ROOT / name
    for item in (path, *path.parents):
        if item.is_symlink() or (hasattr(item, "is_junction") and item.is_junction()):
            raise ValueError(f"Linked paths are not supported: {name}")
    if not path.resolve().is_relative_to(ROOT):
        raise ValueError(f"Path escapes repository: {name}")
    return path


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def json_field_span(text, parts, start=0):
    """Locate a dotted object/array field without reformatting the manifest."""
    decoder = json.JSONDecoder()
    while text[start].isspace():
        start += 1
    if not parts:
        value, end = decoder.raw_decode(text, start)
        valid_version(value)
        return value, (start + 1, end - 1)
    container = text[start]
    cursor, index = start + 1, 0
    while True:
        while cursor < len(text) and (text[cursor].isspace() or text[cursor] == ","):
            cursor += 1
        if cursor >= len(text) or text[cursor] in "}]":
            break
        if container == "{":
            key, cursor = decoder.raw_decode(text, cursor)
            while text[cursor].isspace():
                cursor += 1
            cursor += 1  # colon; syntax has already been validated
            while text[cursor].isspace():
                cursor += 1
        elif container == "[":
            key = str(index)
        else:
            break
        if str(key) == parts[0]:
            return json_field_span(text, parts[1:], cursor)
        _, cursor = decoder.raw_decode(text, cursor)
        index += 1
    raise ValueError("Missing JSON version field: " + ".".join(parts))


def load_targets():
    config = json.loads((ROOT / ".version-bump.json").read_text(encoding="utf-8"))
    if not isinstance(config.get("files"), list) or not config["files"]:
        raise ValueError("Declare at least one version target")
    targets, seen = [], set()
    for entry in config["files"]:
        name, kind, field = entry["path"], entry["format"], entry["field"]
        path = safe_path(name)
        identity = path.resolve()
        if identity in seen:
            raise ValueError(f"Duplicate target: {name}")
        seen.add(identity)
        text = path.read_bytes().decode("utf-8")
        if kind == "text" and field == "version":
            version = valid_version(text.strip())
            start = len(text) - len(text.lstrip())
            span = (start, start + len(version))
        elif kind == "json":
            json.loads(text, object_pairs_hook=unique_object)
            version, span = json_field_span(text, field.split("."))
        elif kind == "yaml" and "." not in field:
            matches = list(re.finditer(r"(?m)^" + re.escape(field) + r":[ \t]*(?P<value>[^\r\n]+?)[ \t]*\r?$", text))
            if len(matches) != 1:
                raise ValueError(f"Expected one YAML version field: {name}")
            value = matches[0]["value"]
            start, end = matches[0].span("value")
            if value[0:1] in {"'", '"'} and value[-1:] == value[0:1]:
                value, start, end = value[1:-1], start + 1, end - 1
            version, span = valid_version(value), (start, end)
        elif kind == "skill" and field == "metadata.version":
            front = re.match(r"\A---\r?\n(?P<body>[\s\S]*?)\r?\n---(?:\r?\n|$)", text)
            if not front:
                raise ValueError(f"Invalid skill frontmatter: {name}")
            metadata = re.findall(r"(?m)^metadata:[ \t]*\r?\n((?:[ \t]+[^\n]*\n?)*)", front["body"])
            if len(metadata) != 1:
                raise ValueError(f"Expected one metadata mapping: {name}")
            matches = list(re.finditer(r'(?m)^  version:[ \t]*(?P<quote>[\"\x27])(?P<value>[^\r\n]+?)(?P=quote)[ \t]*\r?$', metadata[0]))
            if len(matches) != 1:
                raise ValueError(f"Expected one quoted metadata.version: {name}")
            version = valid_version(matches[0]["value"])
            offset = front.start("body") + front["body"].index(metadata[0])
            span = (offset + matches[0].start("value"), offset + matches[0].end("value"))
        else:
            raise ValueError(f"Unsupported target format/field: {kind}/{field}")
        targets.append((name, path, text, span, version))
    return config, targets


def check(targets):
    for name, _, _, _, version in targets:
        print(f"{name}: {version}")
    versions = {entry[4] for entry in targets}
    if len(versions) != 1:
        raise ValueError("Version drift detected; align declared targets before bumping")
    return next(iter(versions))


def audit(config, targets, version):
    declared = {entry[0] for entry in targets}
    excludes = config.get("audit", {}).get("exclude", [])
    pattern = re.compile(r"(?<![0-9A-Za-z_.+-])v?" + re.escape(version) + r"(?![0-9A-Za-z_.+-])")
    hits = []
    for directory, dirs, files in os.walk(ROOT, followlinks=False):
        parent = Path(directory)
        def excluded(name):
            relative = (parent / name).relative_to(ROOT).as_posix()
            return name in {".git", "__pycache__"} or any(fnmatch.fnmatchcase(relative, p) or fnmatch.fnmatchcase(name, p) for p in excludes)
        dirs[:] = [name for name in dirs if not excluded(name) and not (parent / name).is_symlink()
                   and not (hasattr(parent / name, "is_junction") and (parent / name).is_junction())]
        for name in files:
            path = parent / name
            relative = path.relative_to(ROOT).as_posix()
            if relative in declared or excluded(name) or path.is_symlink():
                continue
            try:
                text = path.read_bytes().decode("utf-8")
            except UnicodeDecodeError:
                continue
            if "\0" in text:
                continue
            hits.extend(f"{relative}:{number}: {line}" for number, line in enumerate(text.splitlines(), 1) if pattern.search(line))
    if hits:
        print("Undeclared version references:\n" + "\n".join(hits))
        raise ValueError("Declare these version references or explicitly exclude historical material")
    print("Audit passed: no undeclared current-version references")


def atomic_write(path, data):
    temporary = path.with_name(path.name + ".version-" + uuid.uuid4().hex)
    try:
        temporary.write_bytes(data)
        for attempt in range(5):
            try:
                os.replace(temporary, path)
                break
            except PermissionError as error:
                if getattr(error, "winerror", None) not in {5, 32, 33} or attempt == 4:
                    raise
                time.sleep(0.05 * (2 ** attempt))
    finally:
        temporary.unlink(missing_ok=True)


def update(targets, version):
    originals = {path: text.encode("utf-8") for _, path, text, _, _ in targets}
    try:
        for _, path, text, (start, end), _ in targets:
            updated = (text[:start] + version + text[end:]).encode("utf-8")
            if updated != originals[path]:
                atomic_write(path, updated)
    except Exception:
        for path, data in originals.items():
            if path.read_bytes() != data:
                atomic_write(path, data)
        raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="Validate all declared versions and detect drift")
    mode.add_argument("--audit", action="store_true", help="Check versions and find undeclared current-version references")
    parser.add_argument("version", nargs="?", help="New semantic version, including optional prerelease/build metadata")
    args = parser.parse_args()
    if args.version is not None and (args.check or args.audit):
        parser.error("Choose a new version OR --check/--audit")
    if args.version is None and not (args.check or args.audit):
        parser.print_help()
        return 0
    try:
        if args.version is not None:
            valid_version(args.version)
        config, targets = load_targets()
        current = check(targets)
        if args.audit or args.version is not None:
            audit(config, targets, current)
        if args.version is not None:
            update(targets, args.version)
            print(f"Updated {len(targets)} declared versions: {current} -> {args.version}")
        return 0
    except (ValueError, OSError, KeyError, TypeError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
