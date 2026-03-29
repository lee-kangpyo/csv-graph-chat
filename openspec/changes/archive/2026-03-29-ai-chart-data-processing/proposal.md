## Why

현재 `fix-chart-rendering`에서 구현된 차트 생성 로직은 더미 데이터를 사용한다. "학과별 평균 평점"과 같은 요청 시 실제 CSV 데이터로 groupby/aggregation을 수행하지 않고, 백엔드 코드에서 가상의 라벨과 데이터로 chart config를 생성한다. 이로 인해 사용자에게 의미 없는 차트가 표시된다.

## What Changes

- **백엔드**: LLM이 CSV 헤더와 샘플 데이터를 분석하여 분석 intent 결정
- **백엔드**: 분석 intent를 구조화된 형태로 파싱
- **백엔드**: pandas로 실제 데이터 처리 (groupby, aggregation)
- **백엔드**: 처리 결과를 기반으로 chart config 생성

## Capabilities

### New Capabilities

- `ai-chart-data-processing`: LLM이 CSV 데이터를 분석하여 적절한 차트 데이터를 생성하는 종단 간 플로우
  - LLM: CSV 헤더 + 샘플 10개로 분석 방법 결정
  - 파싱: LLM 응답에서 분석 intent 추출 (group_by, agg_col, agg_func, chart_type)
  - 처리: pandas로 실제 데이터 groupby/aggregation 수행
  - 생성: 처리 결과로 ECharts chart config 생성

### Modified Capabilities

- `ai-chart-generation`: 현재 더미 데이터 기반 처리 → 실제 데이터 기반 처리로 변경
  - 기존: 백엔드 코드에서 고정 데이터로 chart config 생성
  - 변경: LLM intent + pandas 처리로 실제 데이터 기반 chart config 생성

## Impact

- **백엔드**: `app/api/chat.py` - LLM 응답 파싱 로직 추가
- **백엔드**: `app/api/pandas_processor.py` (새 파일) - pandas 처리 로직
- **백엔드**: `app/api/graph_config.py` - pandas_processor 결과로 chart config 생성
- **백엔드**: `app/api/insight_recommendation.py` - LLM 프롬프트 수정
- **백엔드 의존성**: `pandas` 추가 (DuckDB 설치 환경 오류로 인해 pandas로 대체)
