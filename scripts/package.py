"""Prepare a local native-install source. Never touches agent settings or defaults to HOME."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import sys
import uuid
import zipfile

ROOT = Path(__file__).resolve().parents[1]
STATE = ".system-design-state.json"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def payload():
    """Explicit release inventory prevents accidentally shipping caches or credentials."""
    names = json.loads((ROOT / "package-files.json").read_text(encoding="utf-8"))
    result = {}
    for name in names:
        file = checked(ROOT, name)
        if not file.is_file():
            raise ValueError(f"Missing package file: {name}")
        result[name] = file.read_bytes()
    return result


def checked(root, relative):
    """Refuse traversal, symlinks and Windows junctions before accessing owned paths."""
    part = PurePosixPath(relative)
    if not relative or part.is_absolute() or ".." in part.parts or "\\" in relative or ":" in relative:
        raise ValueError(f"Unsafe relative path: {relative}")
    dest = root.joinpath(*part.parts)
    for ancestor in (dest, *dest.parents):
        if ancestor.is_symlink() or (hasattr(ancestor, "is_junction") and ancestor.is_junction()):
            raise ValueError(f"Refusing linked path: {ancestor}")
    if not dest.resolve().is_relative_to(root.resolve()):
        raise ValueError("Path escapes target")
    return dest


def read_state(target):
    file = checked(target, STATE)
    if not file.exists():
        return {}
    data = json.loads(file.read_text(encoding="utf-8"))
    if data.get("package") != "system-design" or data.get("schema") != 1 or not isinstance(data.get("files"), dict):
        raise ValueError("Invalid ownership state; refusing changes")
    for name, sha in data["files"].items():
        checked(target, name)
        if not isinstance(sha, str) or len(sha) != 64 or any(c not in "0123456789abcdef" for c in sha):
            raise ValueError("Invalid ownership digest")
        if name == STATE:
            raise ValueError("State file cannot own itself")
    return data["files"]


def preflight(target, previous, desired):
    for name in previous.keys() | desired.keys():
        file = checked(target, name)
        # Parent files must not become directories implicitly.
        for parent in file.parents:
            if parent.exists() and not parent.is_dir():
                raise ValueError(f"Parent is not a directory: {parent}")
        if file.exists():
            if name not in previous:
                raise ValueError(f"Unowned destination already exists: {name}")
            if not file.is_file() or digest(file.read_bytes()) != previous[name]:
                raise ValueError(f"Owned file was modified; preserve it and resolve manually: {name}")


def atomic_write(file, data):
    file.parent.mkdir(parents=True, exist_ok=True)
    temp = file.with_name(file.name + ".system-design-" + uuid.uuid4().hex)
    try:
        temp.write_bytes(data)
        os.replace(temp, file)
    finally:
        if temp.exists():
            temp.unlink()


def prune_empty_parents(target, names):
    parents = set()
    for name in names:
        path = checked(target, name).parent
        while path != target:
            parents.add(path)
            path = path.parent
    for parent in sorted(parents, key=lambda p: len(p.parts), reverse=True):
        try:
            parent.rmdir()  # Only empty directories; never recursive removal.
        except (FileNotFoundError, OSError):
            pass


def manage(target, remove=False):
    target = Path(os.path.abspath(target))
    checked(target, STATE)  # Check target and all ancestors before resolving links.
    if target == ROOT or target.is_relative_to(ROOT) or ROOT.is_relative_to(target):
        raise ValueError("Target must be separate from and not contain the source package")
    previous = read_state(target)
    desired = {} if remove else {"plugins/system-design/" + name: data for name, data in payload().items()}
    if not remove:
        for name in (".agents/plugins/marketplace.json", ".claude-plugin/marketplace.json"):
            marketplace = json.loads((ROOT / name).read_text(encoding="utf-8"))
            for plugin in marketplace["plugins"]:
                plugin["source"] = {"source": "local", "path": "./plugins/system-design"} if name.startswith(".agents/") else "./plugins/system-design"
            desired[name] = (json.dumps(marketplace, indent=2) + "\n").encode("utf-8")
    preflight(target, previous, desired)
    # Preflight errors cause zero mutation. I/O failures are rolled back within this process.
    originals = {name: checked(target, name).read_bytes() if checked(target, name).exists() else None
                 for name in previous.keys() | desired.keys() | {STATE}}
    try:
        for name, data in desired.items():
            atomic_write(checked(target, name), data)
        for name in previous.keys() - desired.keys():
            checked(target, name).unlink(missing_ok=True)
        if remove:
            checked(target, STATE).unlink(missing_ok=True)
        else:
            state = {"schema": 1, "package": "system-design", "files": {n: digest(d) for n, d in desired.items()}}
            atomic_write(checked(target, STATE), (json.dumps(state, indent=2) + "\n").encode("utf-8"))
    except Exception:
        for name, data in originals.items():
            file = checked(target, name)
            if data is None:
                file.unlink(missing_ok=True)
            else:
                atomic_write(file, data)
        raise
    prune_empty_parents(target, previous.keys() - desired.keys())
    print("Removed owned distribution files" if remove else "Prepared local native-install source")


def pack(output):
    output = Path(output).absolute()
    if output.is_relative_to(ROOT):
        raise ValueError("Archive output must be outside the source package")
    if output.exists():
        raise ValueError("Archive already exists; choose a new output path")
    files = payload()
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "x", compression=zipfile.ZIP_DEFLATED) as archive:
        for name, data in sorted(files.items()):
            archive.writestr("system-design-skill/" + name, data)
    print(f"Packed {len(files)} files")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    subs = parser.add_subparsers(dest="action", required=True)
    for name in ("install", "remove"):
        subs.add_parser(name).add_argument("--target", required=True, type=Path)
    subs.add_parser("pack").add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    try:
        if args.action == "pack":
            pack(args.output)
        else:
            manage(args.target, remove=args.action == "remove")
    except (ValueError, OSError, json.JSONDecodeError) as error:
        print(f"Refused: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
