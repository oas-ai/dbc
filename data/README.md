# DBC data layout

승인된 파생 DBC는 `vehicles/<manufacturer>/<platform>/`에 둡니다. 원본 데이터는 Git에 저장하지 않으며, 각 파일은 registry manifest로 provenance와 SHA-256을 추적합니다.

`vehicles/hyundai/palisade-2020/hyundai_can.dbc`는 commaai/opendbc의 MIT 라이선스
원본을 특정 커밋으로 고정하여 반입한 Hyundai Palisade 2020용 Hyundai legacy CAN
플랫폼 데이터입니다. `CLU11`, `SAS11`, `TCS13`의 canonical 상태 신호와 `CGW1`,
`GW_DDM_PE`, `DATC12`의 raw diagnostics 신호를 DBC 사양대로 해석합니다. upstream의 두
message-comment는 표준 `CM_ BO_` 형식으로 정규화했으며, 메시지·신호 정의는 변경하지 않았습니다.
실차 캡처가 없는 동안에는 이 manifest와 파일 hash를 신뢰 기준으로 삼고, 제어 또는 안전 정책에는
raw diagnostics를 사용하지 않습니다.
