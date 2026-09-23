# DBC validation tools

`uv run --group dev python tools/validate.py`는 registry JSON schema, 파일 경로, SHA-256 및 cantools 구문 분석을 검사합니다. 모든 DBC는 manifest에 등록되어야 하며 data 디렉터리 밖의 파일 참조는 거부됩니다.

`uv run --group dev python -m unittest discover -s tools -p 'test_*.py'`로 반입 경계의 회귀 테스트를 실행합니다. 신호의 실차 일치 여부는 이 검증이 보장하지 않습니다.
