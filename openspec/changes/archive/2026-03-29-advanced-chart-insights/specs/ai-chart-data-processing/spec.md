## Purpose
LLM이 분석 Intent를 기존 단순 group_by/time_series를 넘어서서 복합적인 고급 시각화 Intent 11종(Bar, Line, Scatter, Stacked Bar, Pie, Boxplot, Heatmap, Sankey, Dual Axis, Scatter+VisualMap, Radar)을 결정하고, Pandas 엔진에서 일관된 구조로 데이터를 정제 및 Chart Config로 생성한다.

## Requirements

### Requirement: Unified Intent JSON 구조 정의
LLM이 반환하는 JSON 파라미터 구조는 11종의 차트에서 공통으로 파싱될 수 있도록 통일된 스키마를 가져야 한다.
- **`chart_type`**: 차트 유형 (필수)
- **`x_col`**: X축에 매핑될 기준 컬럼 (가로축 혹은 구분 기준)
- **`y_col`**: Y축 혹은 타겟이 될 기준 컬럼 
- **`category_col`**: 범례 혹은 그룹핑 기준 (색상 구분)
- **`value_col`**: 값 / 도수 / 가중치를 나타내는 숫자 컬럼
- **`agg_func`**: 집계 함수 (count, sum, mean 등)

#### Scenario: 1. 단과대학/학과별 중도탈락(제적) 규모 (Bar)
  - **WHEN** LLM이 제적 비율 확인을 위해 막대 그래프를 제안하면
  - **THEN** 구조: `{"chart_type": "bar", "x_col": "단과대학", "category_col": "학적상태", "value_col": "학생수", "agg_func": "count"}`

#### Scenario: 2. 연도별 학사경고 발생 추이 (Line)
  - **WHEN** 시계열 기반 꺾은선 그래프가 필요하면
  - **THEN** 구조: `{"chart_type": "line", "x_col": "년도", "category_col": "학적상태", "value_col": "학생수", "agg_func": "count"}`

#### Scenario: 3. 이전 전학기 평점과 현재 평점 피어슨 상관 (Scatter)
  - **WHEN** 두 연속형 변수의 인과/상관관계를 파악하려면
  - **THEN** 구조: `{"chart_type": "scatter", "x_col": "전학기 평점", "y_col": "평점", "category_col": "학적상태"}`

#### Scenario: 4. 성별 및 학년별 학사경고 비율 (Stacked Bar)
  - **WHEN** 비율 누적 구조 파악이 필요하면
  - **THEN** 구조: `{"chart_type": "stacked_bar", "x_col": "학년", "category_col": "성별", "value_col": "학사경고횟수", "agg_func": "sum"}`

#### Scenario: 5. 전체 학생 중 누적 학사경고 비율 (Pie)
  - **WHEN** 전체 파이프라인의 총 비중을 볼 때
  - **THEN** 구조: `{"chart_type": "pie", "category_col": "학사경고횟수", "value_col": "학생수", "agg_func": "count"}`

#### Scenario: 6. 성적 하락폭 위험 신호 감지 (Boxplot)
  - **WHEN** 값의 분포 및 이상치 확인이 필요하면
  - **THEN** 구조: `{"chart_type": "boxplot", "x_col": "학적상태", "y_col": "전학기 대비 평점 하락폭"}` (Pandas에서 파생변수 생성 처리)

#### Scenario: 7. 단과대학/학년 병목구간 분석 (Heatmap)
  - **WHEN** 2개의 카테고리 간 밀집도를 볼 때
  - **THEN** 구조: `{"chart_type": "heatmap", "x_col": "학년", "y_col": "단과대학", "value_col": "제적학생수", "agg_func": "count"}`

#### Scenario: 8. 학사경고발생 흐름 - 이탈 경로 (Sankey)
  - **WHEN** 그룹 간 상태 변화나 흐름이 있을 때 (source->target 구조)
  - **THEN** 구조: `{"chart_type": "sankey", "x_col": "원상태(입학/단과대학)", "y_col": "결과상태(제적/경고)", "value_col": "유입원"}`

#### Scenario: 9. 임계점과 전환율 골든타임 파악 (Dual Axis)
  - **WHEN** 학생수 누적(Bar)과 이탈비율 누적(Line) 혼합이 필요하면
  - **THEN** 구조: `{"chart_type": "dual_axis", "x_col": "연속학사경고횟수", "value_col": "누적학생수", "y_col": "이탈비율(%)"}` 

#### Scenario: 10. 성적 반등 그룹 군집/회복력 파악 (Scatter+VisualMap)
  - **WHEN** 차트 기준선 대비 위치기반으로 군집 및 색상을 입혀야 할 때
  - **THEN** 구조: `{"chart_type": "scatter_visualmap", "x_col": "전학기 평점", "y_col": "현재 평점", "category_col": "학적상태"}`

#### Scenario: 11. 집단별 다차원 학사 리스크 지수 비교 (Radar)
  - **WHEN** 여러 기준치들의 종합 스코어 다각형 비교
  - **THEN** 구조: `{"chart_type": "radar", "category_col": "성별", "value_col": ["평균경고횟수", "제적비율", "평균하락폭"]}`

### Requirement: Pandas 통합 데이터 정제
Pandas는 위에서 정의된 Unified Scheme을 파싱하여, 각각의 `chart_type` 전략에 맞추어 연산(count, crosstab, groupby)을 수행하고 ECharts config 형식을 반환해야 한다.
