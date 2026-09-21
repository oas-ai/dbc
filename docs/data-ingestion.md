# DBC 데이터 반입 절차

DBC는 차량 제어·안전과 연결될 수 있는 외부 데이터다. 출처·권한·무결성이 확인되지 않은 DBC를 `main`에 반입하지 않는다.

## 1. 반입 요청

반입 요청에는 제조사, 모델, Platform ID, 모델 연식·지역·powertrain, 데이터 제공자, 취득 경로, 사용·재배포 권한을 기록한다. Platform ID는 `MANUFACTURER_PLATFORM` 형식만 사용하며, 연식과 ADAS 옵션은 metadata로 분리한다.

공개 Issue에는 비공개 계약 정보, 개인 정보, 보안 우회 정보 또는 민감 CAN frame을 게시하지 않는다.

## 2. 원본 보존과 provenance

승인된 원본은 `data/raw/`에 저장하지 않는다. 원본 보관 위치와 접근 권한은 별도 보안 절차로 관리한다. Git에 반입 가능한 파생 DBC는 `data/vehicles/<manufacturer>/<platform>/`에 둔다.

각 반입에는 `data/registry/<platform>.yaml` manifest를 추가한다. manifest에는 원본 식별자, SHA-256, 권한 상태, 검토일, 파생 파일 경로를 포함한다. [schema.json](../data/registry/schema.json)이 manifest 형식을 강제하며, SHA-256은 승인된 파생본이 바뀔 때마다 갱신한다.

## 3. 자동 검증

Pull Request에서는 `uv run --group dev python tools/validate.py`를 실행한다. 이 도구는 Git에 포함된 모든 `.dbc`를 `cantools`로 parse하여 syntax 오류를 차단한다. 프로젝트 고유의 signal naming, counter, checksum 규칙은 검증 규칙이 합의된 뒤 별도 단계로 추가한다.

## 4. 기술·안전 검토

DBC의 signal은 곧바로 OAS API가 되지 않는다. `DBC → CAN Parser → Manufacturer Adapter → OAS Canonical Model` 경계를 유지한다. Vehicle Control 또는 Safety와 연관된 signal은 별도의 Safety review와 실제 log 기반 검증이 필요하다.

## 5. 승인과 변경

PR에는 provenance manifest, validation 결과, 영향을 받는 Adapter/문서를 포함한다. 기존 signal의 이름·scale·offset·enum을 변경하면 compatibility 영향과 migration 계획을 기록한다.
