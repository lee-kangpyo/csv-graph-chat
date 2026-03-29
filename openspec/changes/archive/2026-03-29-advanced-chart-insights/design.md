# System Architecture Updates

기존 아키텍처는 유지하되 데이터 흐름 과정 중 LLM 처리와 Pandas 변환 구간에 "Advanced Intents"라는 새로운 추상화를 도입합니다.

## Component Changes

### 1. `backend/app/api/insight_recommendation.py`
LLM이 생성할 Intent Schema를 대폭 확장합니다.
- 변경 전: `analysis_type`이 `group_by`, `time_series` 중 하나로 제한.
- 변경 후: 추가로 `correlation`, `distribution`, `heatmap`, `flow`, `comparison`, `mixed_axis`, `radar` 등 11개 인사이트를 지원하는 프롬프트를 구성합니다.
  - JSON Schema를 통일하여 `chart_type`, `x_col`, `y_col`, `category_col`, `value_col`, `agg_func` 단일 형태로 11개 차트를 모두 커버하도록 프롬프트 구조화.

### 2. `backend/app/api/pandas_processor.py`
기존에 `process_analysis_intent(df, intent)`가 if-elif 구문으로 단조롭게 돼 있다면 (추정), 이를 확장하여 다양한 `analysis_type` 처리가 가능하도록 변경합니다.
- `scatter`: `df[['X', 'Y', 'Category']]` 병합 추출
- `sankey`: `source`, `target`, `value` 형태의 엣지(`series.links`) 생성
- `heatmap`: `pivot_table` 후 2D 배열(`[[x, y, v], ...]`) 반환 등 Pandas 가공 로직 추가

### 3. `backend/app/api/graph_config.py`
ECharts 생성 함수는 `result`의 데이터를 받아 JSON 구조를 완성합니다. ECharts는 `data`의 구조만 다르게 매핑하면 차트를 렌더링하기 때문에, `pandas_processor.py`에서 전달하는 `result`의 키/벨류를 확장하여 다양한 옵션(`visualMap`, 다중 `series`, `radar` 지표 등)을 동적으로 매핑합니다.

## Data Flow
1. 사용자가 "성적 하락 그룹과 최종 학적변동을 보여줘 (군집 분석)" 입력
2. `insight_recommendation.py`의 `generate_chart_prompt`가 `{"chart_type": "scatter_visualmap", "x_col": "전학기 평점", "y_col": "현재 평점", ...}` Intent 생성
3. `pandas_processor.py`가 DF 기반으로 `[[x, y, 'label'], ...]` 데이터 생성
4. `graph_config.py`가 Scatter 차트 + VisualMap 설정 구조 주입 및 반환
5. 프론트엔드가 ECharts에 렌더링

## Alternatives Considered
- LLM에 아예 모든 ECharts JSON 생성을 맡기는 방안: (현재 프로젝트 방식이 아님) 보안, 일관성, 데이터 유출 문제와 Hallucination이 강하므로 백엔드에서 Pandas로 고정적, 수리적 처리를 하는 방식을 고수합니다.
