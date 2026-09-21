# DBC data layout

승인된 파생 DBC는 `vehicles/<manufacturer>/<platform>/`에 둡니다. 원본 데이터는 Git에 저장하지 않으며, 각 파일은 registry manifest로 provenance와 SHA-256을 추적합니다.

`vehicles/comma/body/comma_body.dbc`는 commaai/opendbc의 MIT 라이선스 원본을
특정 커밋으로 고정하여 반입한 검증용 데이터입니다. 송신 명령 메시지는 사용하지 않으며,
read-only decoding 검증에만 사용합니다.
