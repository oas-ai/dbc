import json
from pathlib import Path

import jsonschema


def test_registry_schema_accepts_a_valid_manifest() -> None:
    schema = json.loads(Path("data/registry/schema.json").read_text(encoding="utf-8"))
    manifest = {
        "platform_id": "GENESIS_RG3",
        "source_id": "approved-source-reference",
        "license_status": "approved",
        "derived_files": [
            {
                "path": "vehicles/genesis/rg3/example.dbc",
                "sha256": "0" * 64,
            }
        ],
        "reviewed_at": "2026-09-21",
    }

    jsonschema.validate(manifest, schema)
