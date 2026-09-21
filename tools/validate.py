"""Git에 반입된 DBC 파일의 최소 syntax 검증을 수행한다."""

from pathlib import Path

import cantools


def main() -> None:
    dbc_files = sorted(Path("data").rglob("*.dbc"))
    for dbc_file in dbc_files:
        cantools.database.load_file(dbc_file)
        print(f"validated: {dbc_file}")
    print(f"validated {len(dbc_files)} DBC file(s)")


if __name__ == "__main__":
    main()
