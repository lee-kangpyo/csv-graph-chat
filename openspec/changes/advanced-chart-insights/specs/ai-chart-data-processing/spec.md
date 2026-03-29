## Purpose
LLM이 분석 Intent를 기존 단순 group_by/time_series를 넘어서서 복합적인 고급 시각화 Intent(산점도, 히트맵, 산키 구조 등)를 결정하고, Pandas 엔진에서 11종 인사이트에 맞게 데이터를 정제 및 Chart Config로 생성한다.

## Requirements

### Requirement: 11가지 고급 인사이트 Intent 생성
LLM은 데이터 타입과 구조를 파악해 11가지의 Advanced Chart Intent 생성을 제안/결정해야 한다.

#### Scenario: 산점도/상관관계 
  - **WHEN** Number 컬럼이 여러 개이고, 두 컬럼 간 관계파악이 필요할 때
  - **THEN** LLM은 `{"analysis_type": "scatter", "chart_type": "scatter", "x_axis": "학점", "y_axis": "결석률", "category": "학적상태"}` 형태를 생성해야 한다.

#### Scenario: 산키 다이어그램 / 흐름 추적
  - **WHEN** 두 개 이상의 범주형 변수 간의 상태 변화(예: 단과대학 -> 경고 1회 -> 제적)가 있을 때
  - **THEN** LLM은 `{"analysis_type": "sankey", "chart_type": "sankey", "source": "단과대학", "target": "학적상태"}` 형태를 생성해야 한다.

#### Scenario: 히트맵 / 분포 분석
  - **WHEN** 두 범주형 변수의 교차 테이블상에서의 밀도를 시각화하려 할 때
  - **THEN** LLM은 `{"analysis_type": "heatmap", "chart_type": "heatmap", "x": "학년", "y": "단과대학", "v": "학생수"}`를 반환해야 한다.

### Requirement: Pandas 확장 데이터 정제
Pandas는 LLM이 결정한 확장된 `analysis_type`에 맞게 DataFrame을 가공하여 반환해야 한다.

#### Scenario: 산점도 데이터 변환 
  - **WHEN** intent가 `scatter`인 경우
  - **THEN** Pandas는 `df[['학점', '결석률', '학적상태']]`를 추출하고 Null 제거 후 ECharts에 필요한 `[[x, y, category], ...]` 폼 형태로 배열을 반환한다.

#### Scenario: Sankey Links/Nodes 리스트 생성
  - **WHEN** intent가 `sankey`인 경우
  - **THEN** Pandas는 각 경로상의 빈도수를 카운트(`groupby([source, target]).size()`)하여 ECharts용 `nodes`와 `links: [{source, target, value}]` 배열을 반환해야 한다.

### Requirement: Dynamic Chart Config 
GraphConfig 매니저는 ECharts 타입에 맞는 옵션 객체(`options`)를 동적 구조화해야 한다.

#### Scenario: 혼합 차트 생성 (Bar & Line)
  - **WHEN** intent가 여러 지표(누적학생수, 제적학생비율)를 가진 혼합차트일 때
  - **THEN** `series`의 첫 번째는 `type: "bar"`, 두 번째는 `type: "line"`으로 병합하고 Secondary yAxis 구조를 `chart_config`에 포함한다.
