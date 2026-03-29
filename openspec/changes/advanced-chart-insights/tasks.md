# Implementation Tasks

## Phase 1: LLM Prompt & Intent Schema Update
- [ ] `backend/app/api/insight_recommendation.py`의 `generate_chart_prompt` 업데이트
  - [ ] 11가지 Advanced Insight 옵션을 LLM이 고를 수 있도록 Prompt Description 보강 (`scatter`, `sankey`, `heatmap`, `mixed_axis` 등)
  - [ ] LLM 반환 JSON 스키마 강화: `x_axis`, `y_axis`, `source_col`, `target_col`, `value_col` 등 차트 타입에 필요한 다양한 키-벨류 포함 매핑.
- [ ] `backend/app/api/insight_recommendation.py`의 `generate_insight_prompt` 수정
  - [ ] 기존 단순 시계열/그룹별 추천 코멘트를 넘어서 통계/군집/흐름 추천 멘트 추가.

## Phase 2: Pandas Data Processing Extension
- [ ] `backend/app/api/pandas_processor.py`에 Intent 처리를 위한 분기 처리 도입
  - [ ] `chart_type == "scatter"` 전략: 세 개 이상의 컬럼 추출 분리 및 NaN 처리
  - [ ] `chart_type == "heatmap"` 전략: 두 컬럼의 pd.crosstab 혹은 pivot 변환 및 2D 배열 리턴
  - [ ] `chart_type == "sankey"` 전략: source/target 노드 정의 및 groupby count edge 생성 리턴
  - [ ] `chart_type == "mixed"` 전략: 독립된 2개의 aggregation 처리 후 병합 (ex. bar, line 누적치)

## Phase 3: ECharts Config Generator Update
- [ ] `backend/app/api/graph_config.py`의 ECharts 옵션 팩토리 업데이트
  - [ ] Scatter, Sankey, Heatmap, Radar에 맞는 `options` 구조 반환 함수 및 로직 추가
  - [ ] 다중 Series 지원 구조 추가 (복수 개의 line, bar)
  - [ ] VisualMap 설정 (데이터에 의존한 색상 옵션) 연동

## Phase 4: Frontend Verification
- [ ] 프론트엔드 React 컴포넌트(`EChartsRenderer` 또는 `ChatArea`)가 새로운 JSON Config 객체를 오류 없이 렌더링하는지 테스트 케이스 구동.
- [ ] Sankey나 Heatmap과 같은 고급 차트를 위한 크기(Width/Height) 비율 조정 대응 추가 작업 확인.
