# Problem / Motivation
현재 `csv-graph-chat` MVP 백엔드에서는 사용자의 데이터에 대해 가장 기초적인 `group_by` (bar/pie)와 `time_series` (line) 두 가지 `analysis_type`에 한정된 분석과 차트 생성만을 지원하고 있습니다 (참고: `backend/app/api/insight_recommendation.py`). 
그러나 실제 비즈니스 혹은 학사 데이터 분석에서는 산점도(Scatter)를 기반으로 한 상관관계 분석, 박스플롯(Boxplot)을 활용한 분포 파악, 히트맵(Heatmap)을 통한 밀집도 확인, 산키 다이어그램(Sankey)을 통한 흐름 분석 등 고도화된 인사이트 도출을 요구합니다. 현재의 LLM 프롬프트 디자인과 pandas 처리 로직은 이러한 복합적인 분석 요청을 소화하지 못해 생성 결과가 단조롭습니다.

# Proposed Solution
현재의 단조로운 AI 차트/인사이트 추천 기능을 고도화하여 11가지 이상의 고급 시각화(Advanced Charts)와 정교한 통계적 연산을 지원하게끔 시스템을 업그레이드합니다.
1. **LLM Prompt 구조화 (Insight Recommendation)**: `insight_recommendation.py`의 `generate_chart_prompt`에 명시된 예시를 대폭 확대합니다. LLM이 `analysis_type`으로 상관관계 분석(`correlation`), 분포도(`distribution`), 흐름 분석(`flow`), 멀티축 비교(`mixed_axis`), 방사형(`radar`) 등 더 다양한 목적을 반환할 수 있도록 프롬프트를 개선합니다.
2. **Pandas 처리 강화 (Data Processing engine)**: `pandas_processor.py`에서 새로운 `analysis_type`을 지원하도록 분기 처리 로직을 추가합니다 (`scatter`, `heatmap`, `boxplot` 형태에 맞는 index/columns 병합, `sankey`를 위한 source-target 엣지 생성 등).
3. **Frontend ECharts 파라미터 매핑 개선**: 백엔드에서 생성된 복잡한 ECharts Config (ex. 다중 Series, 축 매핑, VisualMap 등)를 프론트엔드에서 안정적으로 렌더링하도록 옵션 투입 로직을 튜닝합니다.

# Scope
- `backend/app/api/insight_recommendation.py`의 프롬프트 및 파싱 로직 변경
- `backend/app/api/pandas_processor.py`의 데이터 처리 전략(Strategy) 확장 로직 개발
- `backend/app/api/graph_config.py`의 ECharts 옵션 제네레이터 확대
- `frontend/` ChatArea 및 ECharts 렌더러 컴포넌트 호환성 확인 및 개선

# Not in Scope
- Python 백엔드 아키텍처(FastAPI)의 교체
- LLM 모델 자체의 교체 (현재 구조인 `LLMClient`는 유지)
- 사용자 파일 업로드 구조 변경 (csv-metadata 파싱 로직 유지)
