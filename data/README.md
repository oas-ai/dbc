# DBC data layout

승인된 파생 DBC는 `vehicles/<manufacturer>/<platform>/`에 둡니다. 원본 데이터는 Git에 저장하지 않으며, 각 파일은 registry manifest로 provenance와 SHA-256을 추적합니다.

`vehicles/genesis/g80-2017/hyundai_can.dbc`는 commaai/opendbc의 MIT 라이선스
원본을 특정 커밋으로 고정하여 반입한 Genesis G80 2017용 Hyundai legacy CAN
플랫폼 데이터입니다. `CLU11`, `SAS11`, `TCS13`의 read-only 상태 신호만
decoding 검증에 사용합니다. upstream의 두 message-comment는 표준 `CM_ BO_`
형식으로 정규화했으며, 메시지·신호 정의는 변경하지 않았습니다.
