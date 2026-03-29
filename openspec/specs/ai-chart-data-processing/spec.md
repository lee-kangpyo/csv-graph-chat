## Purpose
LLM이 CSV 데이터를 분석하여 적절한 차트 데이터를 생성하는 종단 간 플로우. CSV 헤더와 샘플 데이터를 기반으로 분석 intent를 결정하고, pandas로 실제 데이터를 처리하여 ECharts chart config를 생성한다.

## Requirements

### Requirement: LLM 분석 intent 결정
시스템은 CSV 헤더와 샘플 데이터를 기반으로 분석 intent를 결정해야 한다.

#### Scenario: group_by 분석
- **WHEN** 사용자가 "학과별 평균 평점"과 같이 그룹화 요청을 하면
- **THEN** LLM은 `{"analysis_type": "group_by", "group_by": "학과", "value": "평점", "agg_func": "mean"}` 형태의 intent를 생성해야 한다

#### Scenario: 시계열 분석
- **WHEN** 사용자가 "월별 추이"와 같이 시계열 요청을 하면
- **THEN** LLM은 `{"analysis_type": "time_series", "time_col": "날짜", "value": "매출", "freq": "monthly"}` 형태의 intent를 생성해야 한다

### Requirement: 분석 intent 파싱
시스템은 LLM 응답에서 분석 intent를 파싱해야 한다.

#### Scenario: JSON 파싱 성공
- **WHEN** LLM 응답에 유효한 JSON intent가 포함되면
- **THEN** 시스템은 intent를 파싱하여 구조화된 형태로 추출해야 한다

#### Scenario: JSON 파싱 실패
- **WHEN** LLM 응답에 유효한 JSON이 없으면
- **THEN** 시스템은 null을 반환하고 차트를 생성하지 않아야 한다

### Requirement: pandas로 데이터 처리
시스템은 분석 intent를 기반으로 pandas로 실제 데이터를 처리해야 한다.

#### Scenario: group_by 처리
- **WHEN** intent가 `group_by` 분석이고 `group_by="학과", agg_func="mean"`이면
- **THEN** 시스템은 `df.groupby('학과')['평점'].mean()`을 실행하고 결과를 반환해야 한다

#### Scenario: aggregation 결과가 비어있음
- **WHEN** pandas 처리 결과가 비어있으면
- **THEN** 시스템은 graph: null을 반환해야 한다

### Requirement: chart config 생성
시스템은 pandas 처리 결과를 ECharts chart config로 변환해야 한다. bar, line, pie, scatter, heatmap, sankey, sunburst 등 모든 ECharts 차트 타입을 지원한다.

#### Scenario: 유효한 처리 결과로 chart 생성
- **WHEN** pandas 처리 결과가 유효하면
- **THEN** 시스템은 ECharts chart config를 생성하여 `graph` 필드에 포함해야 한다

#### Scenario: bar 차트 생성
- **WHEN** intent에 chart_type이 "bar"로 지정되면
- **THEN** 시스템은 series.type이 "bar"인 chart config를 생성해야 한다

#### Scenario: line 차트 생성
- **WHEN** intent에 chart_type이 "line"으로 지정되면
- **THEN** 시스템은 series.type이 "line"인 chart config를 생성해야 한다

#### Scenario: pie 차트 생성
- **WHEN** intent에 chart_type이 "pie"로 지정되면
- **THEN** 시스템은 series.type이 "pie"인 chart config를 생성해야 한다

#### Scenario: scatter 차트 생성
- **WHEN** intent에 chart_type이 "scatter"로 지정되면
- **THEN** 시스템은 series.type이 "scatter"인 chart config를 생성해야 한다

#### Scenario: heatmap 차트 생성
- **WHEN** intent에 chart_type이 "heatmap"으로 지정되면
- **THEN** 시스템은 series.type이 "heatmap"인 chart config를 생성해야 한다
