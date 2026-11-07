import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import unittest
import uuid
from unittest.mock import patch

SOURCE = Path(__file__).resolve().parents[1]


class VersionFixture(unittest.TestCase):
    def setUp(self):
        self.root = Path(__file__).resolve().parent / ("scratch space " + uuid.uuid4().hex)
        self.root.mkdir()
        self.addCleanup(lambda: shutil.rmtree(self.root))
        (self.root / "scripts").mkdir()
        shutil.copyfile(SOURCE / "scripts/bump-version.py", self.root / "scripts/bump-version.py")
        self.skill = self.root / "skills/example/SKILL.md"
        self.skill.parent.mkdir(parents=True)
        self.skill.write_text('---\nname: example\ndescription: Example\nmetadata:\n  version: "1.2.3"\n---\nBody stays untouched.\n', encoding="utf-8")
        (self.root / "VERSION").write_text("1.2.3\n", encoding="utf-8")
        self.config = {"files": [{"path": "VERSION", "format": "text", "field": "version"},
                                  {"path": "skills/example/SKILL.md", "format": "skill", "field": "metadata.version"}],
                       "audit": {"exclude": ["RELEASE-NOTES.md"]}}
        self.save_config()

    def save_config(self):
        (self.root / ".version-bump.json").write_text(json.dumps(self.config), encoding="utf-8")

    def run_script(self, *args, ok=True):
        result = subprocess.run([sys.executable, "-X", "utf8", str(self.root / "scripts/bump-version.py"), *args],
                                cwd=self.root.parent, capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(result.returncode == 0, ok, result.stdout + result.stderr)
        return result


class VersioningTests(VersionFixture):
    def test_check_bump_repeat_and_content_preservation(self):
        self.run_script("--check")
        self.run_script("--audit")
        self.run_script("2.0.0-rc.1+build.4")
        self.assertEqual((self.root / "VERSION").read_text(), "2.0.0-rc.1+build.4\n")
        self.assertIn('version: "2.0.0-rc.1+build.4"', self.skill.read_text())
        self.assertTrue(self.skill.read_text().endswith("Body stays untouched.\n"))
        before = self.skill.read_bytes()
        self.run_script("2.0.0-rc.1+build.4")
        self.assertEqual(before, self.skill.read_bytes())

    def test_drift_blocks_check_audit_and_bump(self):
        self.skill.write_text(self.skill.read_text().replace("1.2.3", "1.2.4"))
        before = (self.root / "VERSION").read_bytes()
        for action in ("--check", "--audit", "2.0.0"):
            self.run_script(action, ok=False)
        self.assertEqual((self.root / "VERSION").read_bytes(), before)

    def test_invalid_semver_is_rejected_without_changes(self):
        before = self.skill.read_bytes()
        for version in ("1.2", "01.2.3", "1.2.3garbage", "1.2.3-01", "1.2.3+", "v1.2.3"):
            self.run_script(version, ok=False)
        self.assertEqual(before, self.skill.read_bytes())

    def test_missing_or_invalid_target_blocks_all_writes(self):
        self.skill.unlink()
        self.run_script("2.0.0", ok=False)
        self.assertEqual((self.root / "VERSION").read_text(), "1.2.3\n")

    def test_audit_finds_pins_ignores_ip_and_excluded_history(self):
        (self.root / "host.txt").write_text("host=10.1.2.3\n", encoding="utf-8")
        (self.root / "RELEASE-NOTES.md").write_text("Version 1.2.3\n", encoding="utf-8")
        self.run_script("--audit")
        (self.root / "pin.txt").write_text("release#v1.2.3\n", encoding="utf-8")
        self.assertIn("pin.txt", self.run_script("--audit", ok=False).stdout)
        self.run_script("2.0.0", ok=False)
        self.assertEqual((self.root / "VERSION").read_text(), "1.2.3\n")

    def test_path_escape_and_duplicate_config_are_rejected(self):
        self.config["files"].append({"path": "../outside", "format": "text", "field": "version"})
        self.save_config()
        self.run_script("--check", ok=False)
        self.config["files"][-1] = self.config["files"][0]
        self.save_config()
        self.run_script("--check", ok=False)

    def test_numeric_metadata_is_rejected(self):
        self.skill.write_text(self.skill.read_text().replace('"1.2.3"', "123"))
        self.run_script("2.0.0", ok=False)
        self.assertEqual((self.root / "VERSION").read_text(), "1.2.3\n")

    def test_write_failure_rolls_back_earlier_changes(self):
        spec = importlib.util.spec_from_file_location("version_tool", self.root / "scripts/bump-version.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        _, targets = module.load_targets()
        original = {path: path.read_bytes() for _, path, *_ in targets}
        actual_replace = module.os.replace
        calls = 0
        def fail_once(source, target):
            nonlocal calls
            calls += 1
            if calls == 2:
                raise OSError("simulated replacement failure")
            return actual_replace(source, target)
        with patch.object(module.os, "replace", side_effect=fail_once):
            with self.assertRaises(OSError):
                module.update(targets, "2.0.0")
        self.assertTrue(all(path.read_bytes() == data for path, data in original.items()))

    def test_transient_windows_lock_is_retried(self):
        spec = importlib.util.spec_from_file_location("version_tool_retry", self.root / "scripts/bump-version.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        actual_replace = module.os.replace
        calls = 0
        def locked_once(source, target):
            nonlocal calls
            calls += 1
            if calls == 1:
                error = PermissionError("temporary Windows sharing lock")
                error.winerror = 32
                raise error
            return actual_replace(source, target)
        with patch.object(module.os, "replace", side_effect=locked_once):
            module.atomic_write(self.root / "VERSION", b"2.0.0\n")
        self.assertEqual((self.root / "VERSION").read_bytes(), b"2.0.0\n")
        self.assertEqual(calls, 2)

    def test_persistent_windows_lock_stops_after_bounded_attempts(self):
        spec = importlib.util.spec_from_file_location("version_tool_lock", self.root / "scripts/bump-version.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        error = PermissionError("persistent Windows sharing lock")
        error.winerror = 32
        original = (self.root / "VERSION").read_bytes()
        with patch.object(module.os, "replace", side_effect=error) as replace, patch.object(module.time, "sleep"):
            with self.assertRaises(PermissionError):
                module.atomic_write(self.root / "VERSION", b"2.0.0\n")
        self.assertEqual(replace.call_count, 5)
        self.assertEqual((self.root / "VERSION").read_bytes(), original)


if __name__ == "__main__":
    unittest.main(verbosity=2)
