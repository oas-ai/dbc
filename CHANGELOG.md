# Changelog

## Unreleased

- Reject unregistered DBC files and manifest paths outside the data directory; test hash and path boundaries in CI.

- Add a Palisade 2020 listen-only capture-validation template for DBC raw diagnostics.
- Treat the provenance-pinned Palisade DBC as the current signal specification for read-only raw diagnostics pending vehicle captures.
- Add the MIT-licensed Hyundai Palisade 2020 Hyundai legacy CAN DBC as a provenance-tracked read-only sample.

## [0.1.0] - 2026-09-21

- DBC 데이터 반입 절차와 검증 도구 기반을 추가했습니다.
- Provenance manifest schema 및 SHA-256 검증을 추가했습니다.
