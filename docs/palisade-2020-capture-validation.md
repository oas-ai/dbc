# Hyundai Palisade 2020 capture validation

이 절차는 provenance-pinned `hyundai_can.dbc`의 read-only raw diagnostics 가정을 실차에서
확인할 때 사용한다. 차량에 CAN frame을 송신하지 않으며, 주행 중 조작이나 안전·제어 기능 검증을
포함하지 않는다.

## 대상과 사전 조건

- 정차·시동 ON 상태에서 listen-only SocketCAN interface를 사용한다.
- 차량 식별 번호, 위치, 사람의 영상·음성, 계정 정보는 기록하지 않는다.
- 원본 로그는 Git에 넣지 않고 승인된 보안 저장소에 보관한다. Git에는 아래 요약만 남긴다.

| DBC message | 확인 신호 | 관찰할 상태 |
| --- | --- | --- |
| `CGW1` (`0x541`) | `CF_Gway_DrvDrSw`, 앞좌석 belt switch | 운전석 도어·앞좌석 벨트 상태 변화 |
| `GW_DDM_PE` (`0x521`) | 네 `*DoorStatus` | 각 도어를 한 번씩 분리하여 변화 |
| `DATC12` (`0x042`) | 앞좌석 `*TempDispC` | 각 좌석 설정 온도를 0.5°C 단위로 변화 |

## 수신과 기록

수신 장치를 먼저 listen-only로 확인한 뒤 대상 ID만 기록한다.

```sh
ip -details link show can0
candump -L -t a can0,541:7FF,521:7FF,042:7FF > palisade-2020-raw.log
```

상태를 하나만 바꾸고, 각 변화 전후의 timestamp와 관찰 결과를 별도 표에 적는다. 아래 템플릿의
`payload`는 보안 저장소의 log offset 또는 허가된 축약값을 가리키며, 공개 문서에 원본 frame을
복사하지 않는다.

| capture id | DBC message.signal | 관찰 상태 | DBC physical value | payload reference | reviewer |
| --- | --- | --- | --- | --- | --- |
| `YYYY-MM-DD-session-N` | `DATC12.CR_Datc_DrTempDispC` | 운전석 20.0°C | `20.0` | secure-log offset | pending |

## 판정

1. message ID, bit 위치, scale/offset이 관찰 상태 변화와 반복해서 일치하면 raw diagnostics
   catalog의 DBC 신뢰 상태를 `observed`로 갱신한다.
2. 불일치하거나 enum의 의미가 모호하면 해당 signal은 raw catalog에서 유지하되, canonical state와
   제어·안전 정책으로 승격하지 않는다.
3. 관찰 요약, DBC revision, 차량 연식·트림 범위(식별 가능한 정보 제외), reviewer를 PR에 기록한다.
   원본 log와 개인·차량 식별 정보는 첨부하지 않는다.
