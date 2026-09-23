import hashlib
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import validate
import yaml


class ManifestTest(unittest.TestCase):
    def test_hash_and_path_boundary(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            data = root / "data"
            data.mkdir()
            source = data / "example.dbc"
            source.write_bytes(b"synthetic")
            manifest = data / "manifest.yaml"
            entry = {
                "path": "example.dbc",
                "sha256": hashlib.sha256(b"synthetic").hexdigest(),
            }
            with patch.object(validate, "DATA_DIRECTORY", data):
                manifest.write_text(yaml.safe_dump({"derived_files": [entry]}))
                self.assertEqual(
                    validate.validate_registry_manifest(manifest, {}),
                    {source.resolve()},
                )
                source.write_bytes(b"changed")
                with self.assertRaisesRegex(ValueError, "SHA-256 mismatch"):
                    validate.validate_registry_manifest(manifest, {})
                entry["path"] = "../outside.dbc"
                manifest.write_text(yaml.safe_dump({"derived_files": [entry]}))
                with self.assertRaisesRegex(ValueError, "escapes"):
                    validate.validate_registry_manifest(manifest, {})


if __name__ == "__main__":
    unittest.main()
