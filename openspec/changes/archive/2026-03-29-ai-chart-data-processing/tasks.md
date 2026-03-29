## 1. LLM 프롬프트 및 응답 처리

- [x] 1.1 `insight_recommendation.py`에 `generate_chart_prompt()` 함수 추가
- [x] 1.2 LLM 응답에서 JSON intent 파싱 함수 추가
- [x] 1.3 파싱 실패 시 fallback 로직 추가

## 2. pandas 처리 모듈

- [x] 2.1 `pandas_processor.py` 모듈 생성
- [x] 2.2 `process_group_by()` 함수 구현
- [x] 2.3 `process_time_series()` 함수 구현
- [x] 2.4 pandas 처리 결과 검증 로직 추가

## 3. chat.py 통합

- [x] 3.1 `chat.py`에서 LLM 응답 파싱 로직 추가
- [x] 3.2 pandas_processor 호출 로직 추가
- [x] 3.3 chart config 생성 로직 수정

## 4. 테스트

- [x] 4.1 LLM intent 파싱 및 생성 테스트
  - [x] 4.1.1 JSON 파싱 테스트 (완료)
  - [x] 4.1.2 LLM intent 생성 프로세스 테스트 (완료)

- [x] 4.2 pandas 데이터 처리 테스트
  - [x] 4.2.1 group_by 처리 테스트 (완료)
  - [x] 4.2.2 time_series 처리 테스트 (완료)

- [x] 4.3 chart config 생성 테스트
  - [x] 4.3.1 bar 차트 테스트 (완료)
  - [x] 4.3.2 line 차트 테스트 (완료)
  - [x] 4.3.3 pie 차트 테스트 (완료)
  - [x] 4.3.4 scatter 차트 테스트 (완료)
  - [x] 4.3.5 heatmap 차트 테스트 (완료)

- [x] 4.4 end-to-end 통합 테스트
  - [x] 4.4.1 LLM → 파싱 → pandas → chart config 전체 흐름 테스트 (완료)
