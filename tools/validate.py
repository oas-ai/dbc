"""Git에 반입된 DBC 파일의 최소 syntax 검증을 수행한다."""

import hashlib
import json
from collections.abc import Mapping
from pathlib import Path
from typing import Any

import cantools
import jsonschema
import yaml

DATA_DIRECTORY = Path("data")
REGISTRY_DIRECTORY = DATA_DIRECTORY / "registry"


def validate_registry_manifest(manifest_path: Path, schema: Mapping[str, Any]) -> None:
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    jsonschema.validate(manifest, schema)

    for derived_file in manifest["derived_files"]:
        file_path = DATA_DIRECTORY / derived_file["path"]
        if not file_path.is_file():
            raise ValueError(f"missing derived file: {file_path}")
        with file_path.open("rb") as data_file:
            actual_sha256 = hashlib.file_digest(data_file, "sha256").hexdigest()
        if actual_sha256 != derived_file["sha256"]:
            raise ValueError(f"SHA-256 mismatch: {file_path}")


def main() -> None:
    schema = json.loads(
        (REGISTRY_DIRECTORY / "schema.json").read_text(encoding="utf-8")
    )
    manifest_paths = sorted(REGISTRY_DIRECTORY.glob("*.yaml"))
    for manifest_path in manifest_paths:
        validate_registry_manifest(manifest_path, schema)
        print(f"validated manifest: {manifest_path}")

    dbc_files = sorted(DATA_DIRECTORY.rglob("*.dbc"))
    for dbc_file in dbc_files:
        cantools.database.load_file(dbc_file)
        print(f"validated: {dbc_file}")
    print(
        f"validated {len(manifest_paths)} manifest(s) and {len(dbc_files)} DBC file(s)"
    )


if __name__ == "__main__":
    main()
