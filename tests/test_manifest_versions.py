"""Exercise synchronized release versions across the installable package."""
import json
from pathlib import Path

from test_versioning import VersionFixture


class ManifestVersionTests(VersionFixture):
    def add_manifests(self):
        (self.root / "package.json").write_text('{"name":"example","version":"1.2.3"}\n', encoding="utf-8")
        (self.root / "marketplace.json").write_text('{"plugins":[{"version":"1.2.3"}]}\n', encoding="utf-8")
        (self.root / "plugin.yaml").write_text('name: example\nversion: "1.2.3"\n', encoding="utf-8")
        self.config["files"] += [
            {"path":"package.json", "format":"json", "field":"version"},
            {"path":"marketplace.json", "format":"json", "field":"plugins.0.version"},
            {"path":"plugin.yaml", "format":"yaml", "field":"version"},
        ]
        self.save_config()

    def test_bump_updates_json_nested_arrays_yaml_and_skill(self):
        self.add_manifests()
        self.run_script("2.0.0")
        self.assertEqual(json.loads((self.root / "package.json").read_text())["version"], "2.0.0")
        self.assertEqual(json.loads((self.root / "marketplace.json").read_text())["plugins"][0]["version"], "2.0.0")
        self.assertIn('version: "2.0.0"', (self.root / "plugin.yaml").read_text())
        self.run_script("--audit")

    def test_invalid_manifest_prevents_partial_updates(self):
        self.add_manifests()
        (self.root / "plugin.yaml").write_text("version: 123\n", encoding="utf-8")
        self.run_script("2.0.0", ok=False)
        self.assertEqual((self.root / "VERSION").read_text(), "1.2.3\n")
        self.assertEqual(json.loads((self.root / "package.json").read_text())["version"], "1.2.3")

    def test_missing_nested_field_prevents_partial_updates(self):
        self.add_manifests()
        (self.root / "marketplace.json").write_text('{"plugins":[]}', encoding="utf-8")
        self.run_script("2.0.0", ok=False)
        self.assertEqual((self.root / "VERSION").read_text(), "1.2.3\n")
