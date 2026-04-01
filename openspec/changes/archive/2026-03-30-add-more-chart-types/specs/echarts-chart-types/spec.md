## ADDED Requirements

### Requirement: TestChartPage supports all major ECharts chart types
테스트 페이지는 기존 7개에 이어 12개 이상의 추가 차트 유형 preset을 제공해야 한다. (SHALL)

#### Scenario: Radar chart preset selection
- **WHEN** 사용자가 "Radar Chart" preset을 선택하면
- **THEN** GraphView에 radar chart가 샘플 데이터와 함께 렌더링된다

#### Scenario: Polar chart preset selection
- **WHEN** 사용자가 "Polar Chart" preset을 선택하면
- **THEN** GraphView에 polar chart가 샘플 데이터와 함께 렌더링된다

#### Scenario: Graph chart preset selection
- **WHEN** 사용자가 "Graph Chart" preset을 선택하면
- **THEN** GraphView에 graph chart가 샘플 데이터와 함께 렌더링된다

#### Scenario: Tree chart preset selection
- **WHEN** 사용자가 "Tree Chart" preset을 선택하면
- **THEN** GraphView에 tree chart가 샘플 데이터와 함께 렌더링된다

#### Scenario: Sunburst chart preset selection
- **WHEN** 사용자가 "Sunburst Chart" preset을 선택하면
- **THEN** GraphView에 sunburst chart가 샘플 데이터와 함께 렌더링된다

#### Scenario: Treemap chart preset selection
- **WHEN** 사용자가 "Treemap Chart" preset을 선택하면
- **THEN** GraphView에 treemap chart가 샘플 데이터와 함께 렌더링된다

#### Scenario: Parallel chart preset selection
- **WHEN** 사용자가 "Parallel Chart" preset을 선택하면
- **THEN** GraphView에 parallel chart가 샘플 데이터와 함께 렌더링된다

#### Scenario: Gauge chart preset selection
- **WHEN** 사용자가 "Gauge Chart" preset을 선택하면
- **THEN** GraphView에 gauge chart가 샘플 데이터와 함께 렌더링된다

#### Scenario: Funnel chart preset selection
- **WHEN** 사용자가 "Funnel Chart" preset을 선택하면
- **THEN** GraphView에 funnel chart가 샘플 데이터와 함께 렌더링된다

#### Scenario: Candlestick chart preset selection
- **WHEN** 사용자가 "Candlestick Chart" preset을 선택하면
- **THEN** GraphView에 candlestick chart가 샘플 데이터와 함께 렌더링된다

#### Scenario: Calendar chart preset selection
- **WHEN** 사용자가 "Calendar Chart" preset을 선택하면
- **THEN** GraphView에 calendar chart가 샘플 데이터와 함께 렌더링된다

### Requirement: Each chart preset includes realistic sample data
각 차트 preset은 해당 차트 유형에 적합한 현실적인 샘플 데이터를 포함해야 한다. (SHALL)

#### Scenario: Verify sample data is chart-type appropriate
- **WHEN** 사용자가 차트 preset을 확인하면
- **THEN** 샘플 데이터가 차트 유형 요구사항에 적합해야 한다 (예: radar는 indicator 데이터, candlestick는 OHLC 데이터)

### Requirement: Config JSON section is collapsed by default
Config JSON 섹션은 페이지 로드 시 기본적으로 접혀 있어야 하며, 차트가 바로 표시되어야 한다. (SHALL)

#### Scenario: Page loads with config collapsed
- **WHEN** 사용자가 TestChartPage에 접속하면
- **THEN** Config JSON 섹션이 기본적으로 접혀 있다
- **AND** 차트가 바로 보인다

#### Scenario: Toggle config section visibility
- **WHEN** 사용자가 토글 버튼을 클릭하면
- **THEN** Config JSON 섹션이 expand/collapse 된다
- **AND** 기존 config 내용이 유지된다

### Requirement: Current Config section is collapsed by default
현재 Config 섹션도 기본적으로 접혀 있어야 한다. (SHALL)

#### Scenario: Page loads with current config collapsed
- **WHEN** 사용자가 TestChartPage에 접속하면
- **THEN** 현재 Config 섹션이 기본적으로 접혀 있다

#### Scenario: Toggle current config section visibility
- **WHEN** 사용자가 현재 Config 토글 버튼을 클릭하면
- **THEN** 현재 Config 섹션이 expand/collapse 된다
