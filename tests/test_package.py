"""Offline package checks. No application or model runtime is invoked."""
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
import uuid
import re
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]


class DistributionTests(unittest.TestCase):
    def setUp(self):
        temp_root = ROOT.parent / ".system-design-test-temp"
        temp_root.mkdir(exist_ok=True)
        directory = temp_root / ("system design проверка " + uuid.uuid4().hex)
        directory.mkdir()
        self.temp = SimpleNamespace(name=str(directory))
        self.addCleanup(lambda: shutil.rmtree(directory) if directory.exists() else None)
        self.target = Path(self.temp.name) / "поставка с пробелами"

    def command(self, *args, ok=True):
        result = subprocess.run([sys.executable, "-X", "utf8", str(ROOT / "scripts/package.py"), *map(str, args)],
                                capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(result.returncode == 0, ok, result.stdout + result.stderr)
        return result

    def install(self):
        self.command("install", "--target", self.target)
        return self.target / "plugins/system-design"

    def test_validator(self):
        result = subprocess.run([sys.executable, str(ROOT / "scripts/validate.py")], capture_output=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_installed_reference_tree_uses_fictional_identifiers(self):
        tree = (ROOT / "skills/system-design-enter/references/project-tree.md").read_text(encoding="utf-8")
        self.assertIn("HarborDesk/", tree)
        self.assertIn("harbor_desk/", tree)
        original = ROOT.parent / "system-design/references/project-tree.md"
        if original.is_file():
            original_text = original.read_text(encoding="utf-8")
            original_project = re.search(r"```text\n([^/\n]+)/", original_text).group(1)
            original_module = re.search(r"src/([^/\n]+)/", original_text).group(1)
            for file in (ROOT / "skills").rglob("*.md"):
                text = file.read_text(encoding="utf-8").casefold()
                self.assertNotIn(original_project.casefold(), text, str(file))
                self.assertNotIn(original_module.casefold(), text, str(file))

    def test_subject_references_are_packaged_and_reachable_from_skills(self):
        subjects = {"domain-discovery.md", "context-relationships.md", "relationship-mechanisms.md",
                    "design-patterns.md", "architecture-patterns.md", "review-method.md", "review-report.md",
                    "planning-method.md", "planning-example.md", "question-rounds.md", "methodology.md"}
        refs = ROOT / "skills/system-design-enter/references"
        self.assertTrue(all((refs / name).is_file() for name in subjects))
        reached, pending = set(), list((ROOT / "skills").glob("*/SKILL.md"))
        while pending:
            file = pending.pop().resolve()
            if file in reached:
                continue
            reached.add(file)
            for link in re.findall(r"\]\(([^)]+)\)", file.read_text(encoding="utf-8")):
                if "://" not in link and not link.startswith("#"):
                    target = (file.parent / link.split("#")[0]).resolve()
                    if target.suffix == ".md" and target.is_file():
                        pending.append(target)
        self.assertTrue({(refs / name).resolve() for name in subjects}.issubset(reached))

    def test_validator_rejects_invalid_ids_missing_manifest_paths_and_local_paths(self):
        source = Path(self.temp.name) / "mutated package"
        shutil.copytree(ROOT, source, ignore=shutil.ignore_patterns("__pycache__", ".git"))
        spec = importlib.util.spec_from_file_location("validate_package", ROOT / "scripts/validate.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.assertEqual(module.validate(source), [])
        skill = source / "skills/system-design-enter/SKILL.md"
        skill.write_text(skill.read_text(encoding="utf-8").replace("name: system-design-enter", "name: Invalid:Name"), encoding="utf-8")
        self.assertTrue(any("frontmatter" in e for e in module.validate(source)))
        manifest = source / ".cursor-plugin/plugin.json"
        data = json.loads(manifest.read_text(encoding="utf-8"))
        data["hooks"] = "./missing-hook.json"
        manifest.write_text(json.dumps(data), encoding="utf-8")
        self.assertTrue(any("manifest path" in e for e in module.validate(source)))
        doc = source / "README.md"
        doc.write_text("Developer checkout: " + "Z:" + "/" + "Users/example/work", encoding="utf-8")
        self.assertTrue(any("local absolute path" in e for e in module.validate(source)))

    def test_repeat_install_and_remove_preserve_unrelated_files(self):
        plugin = self.install()
        extra = plugin / "user-notes.txt"
        extra.write_text("keep", encoding="utf-8")
        outside = self.target / "unrelated.txt"
        outside.write_text("keep", encoding="utf-8")
        self.install()
        self.command("remove", "--target", self.target)
        self.assertEqual(extra.read_text(), "keep")
        self.assertTrue(outside.exists())
        self.assertFalse((plugin / "skills/system-design-review/SKILL.md").exists())
        self.command("remove", "--target", self.target)

    def test_modified_owned_file_blocks_update_and_removal_before_mutation(self):
        plugin = self.install()
        owned = plugin / "skills/system-design-enter/SKILL.md"
        owned.write_text("user edit", encoding="utf-8")
        marker = self.target / ".agents/plugins/marketplace.json"
        before = marker.read_bytes()
        self.command("install", "--target", self.target, ok=False)
        self.command("remove", "--target", self.target, ok=False)
        self.assertEqual(owned.read_text(), "user edit")
        self.assertEqual(marker.read_bytes(), before)

    def test_existing_marketplace_collision_is_preserved(self):
        path = self.target / ".agents/plugins/marketplace.json"
        path.parent.mkdir(parents=True)
        path.write_text('{"name":"user"}', encoding="utf-8")
        self.command("install", "--target", self.target, ok=False)
        self.assertEqual(path.read_text(), '{"name":"user"}')
        self.assertFalse((self.target / "plugins").exists())

    def test_update_replaces_owned_files_and_prunes_only_owned_obsolete_files(self):
        self.install()
        state_file = self.target / ".system-design-state.json"
        state = json.loads(state_file.read_text(encoding="utf-8"))
        obsolete = self.target / "plugins/system-design/obsolete.txt"
        obsolete.write_bytes(b"old version")
        state["files"]["plugins/system-design/obsolete.txt"] = hashlib.sha256(obsolete.read_bytes()).hexdigest()
        # Model a previous release inventory, without editing the source package.
        path = self.target / "plugins/system-design/README.md"
        path.write_bytes(b"previous release")
        state["files"]["plugins/system-design/README.md"] = hashlib.sha256(path.read_bytes()).hexdigest()
        state_file.write_text(json.dumps(state), encoding="utf-8")
        self.install()
        self.assertFalse(obsolete.exists())
        self.assertEqual(path.read_bytes(), (ROOT / "README.md").read_bytes())

    def test_state_traversal_is_rejected(self):
        self.install()
        state_file = self.target / ".system-design-state.json"
        state = json.loads(state_file.read_text(encoding="utf-8"))
        state["files"]["../outside.txt"] = "0" * 64
        state_file.write_text(json.dumps(state), encoding="utf-8")
        self.command("remove", "--target", self.target, ok=False)

    def test_target_inside_source_is_rejected(self):
        self.command("install", "--target", ROOT / "nested-target", ok=False)
        self.assertFalse((ROOT / "nested-target").exists())

    def test_archive_is_relocatable_and_independent(self):
        archive = Path(self.temp.name) / "release.zip"
        self.command("pack", "--output", archive)
        unpacked = Path(self.temp.name) / "isolated"
        with zipfile.ZipFile(archive) as zf:
            self.assertTrue(all(not name.startswith(("/", "..")) for name in zf.namelist()))
            zf.extractall(unpacked)
        isolated = unpacked / "system-design-skill"
        result = subprocess.run([sys.executable, str(isolated / "scripts/validate.py")], capture_output=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        result = subprocess.run([sys.executable, str(isolated / "scripts/package.py"), "install", "--target",
                                 str(Path(self.temp.name) / "standalone")], capture_output=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_symlink_in_owned_path_is_rejected(self):
        self.target.mkdir()
        outside = Path(self.temp.name) / "outside"
        outside.mkdir()
        try:
            (self.target / "plugins").symlink_to(outside, target_is_directory=True)
        except OSError:
            self.skipTest("Creating symlinks is unavailable on this Windows account")
        self.command("install", "--target", self.target, ok=False)
        self.assertEqual(list(outside.iterdir()), [])


class HermesTests(unittest.TestCase):
    def test_register_and_first_turn_contract(self):
        spec = importlib.util.spec_from_file_location("system_design_hermes", ROOT / ".hermes-plugin/__init__.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        class Context:
            def __init__(self):
                self.skills, self.hooks = {}, {}
            def register_skill(self, name, path, description):
                assert isinstance(path, Path) and path.is_file() and description
                self.skills[name] = path
            def register_hook(self, name, callback):
                self.hooks[name] = callback
        ctx = Context()
        module.register(ctx)
        self.assertEqual(len(ctx.skills), 5)
        hook = ctx.hooks["pre_llm_call"]
        self.assertIn("Static review", hook(is_first_turn=True)["context"])
        self.assertIsNone(hook(is_first_turn=False))
        self.assertIsNone(hook(is_first_turn=True, platform="subagent"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
