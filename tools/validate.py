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


def validate_registry_manifest(
    manifest_path: Path, schema: Mapping[str, Any]
) -> set[Path]:
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    jsonschema.validate(manifest, schema)

    registered = set()
    for derived_file in manifest["derived_files"]:
        file_path = (DATA_DIRECTORY / derived_file["path"]).resolve()
        if not file_path.is_relative_to(DATA_DIRECTORY.resolve()):
            raise ValueError(f"derived file escapes data directory: {file_path}")
        if not file_path.is_file():
            raise ValueError(f"missing derived file: {file_path}")
        with file_path.open("rb") as data_file:
            actual_sha256 = hashlib.file_digest(data_file, "sha256").hexdigest()
        if actual_sha256 != derived_file["sha256"]:
            raise ValueError(f"SHA-256 mismatch: {file_path}")
        registered.add(file_path)
    return registered


def main() -> None:
    schema = json.loads(
        (REGISTRY_DIRECTORY / "schema.json").read_text(encoding="utf-8")
    )
    manifest_paths = sorted(REGISTRY_DIRECTORY.glob("*.yaml"))
    registered = set()
    for manifest_path in manifest_paths:
        registered.update(validate_registry_manifest(manifest_path, schema))
        print(f"validated manifest: {manifest_path}")

    dbc_files = sorted(DATA_DIRECTORY.rglob("*.dbc"))
    for dbc_file in dbc_files:
        if dbc_file.resolve() not in registered:
            raise ValueError(f"DBC has no provenance manifest: {dbc_file}")
        cantools.database.load_file(dbc_file)
        print(f"validated: {dbc_file}")
    print(
        f"validated {len(manifest_paths)} manifest(s) and {len(dbc_files)} DBC file(s)"
    )


if __name__ == "__main__":
    main()
