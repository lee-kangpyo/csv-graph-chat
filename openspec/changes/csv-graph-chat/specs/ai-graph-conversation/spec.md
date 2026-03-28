## ADDED Requirements

### Requirement: AI insight recommendation
After analyzing CSV data, the system SHALL have AI ask users which insights they want to see.

#### Scenario: AI recommends insights based on data types
- **WHEN** CSV has Date + Number columns
- **THEN** AI SHALL recommend "시계열 추이" (time series trend)
- **AND** offer options like monthly/quarterly/yearly comparison

#### Scenario: AI recommends group comparison
- **WHEN** CSV has Category + Number columns
- **THEN** AI SHALL recommend "그룹별 비교" (group comparison)
- **AND** suggest bar charts or pie charts

#### Scenario: AI offers custom insight option
- **WHEN** AI presents recommended insights
- **THEN** AI SHALL also offer "직접 설명해주세요" (please explain directly)
- **AND** wait for user's custom request

### Requirement: Natural language graph modification
The system SHALL allow users to modify graphs using natural language commands.

#### Scenario: Change chart type
- **WHEN** user says "지역별로 나눠줘" or "막대 그래프로 바꿔줘"
- **THEN** system SHALL update the graph accordingly
- **AND** confirm the change

#### Scenario: Change colors/style
- **WHEN** user says "색깔 바꿔줘" or "파란색으로 해줘"
- **THEN** system SHALL update the chart colors
- **AND** show the modified graph

#### Scenario: Filter data range
- **WHEN** user says "1월만 보여줘" or "이상치 제외해줘"
- **THEN** system SHALL update the graph to show filtered data
- **AND** confirm the filter applied

#### Scenario: Add trend line
- **WHEN** user says "trend line 추가해줘"
- **THEN** system SHALL add a trend line to the existing chart

### Requirement: Real-time streaming response
The system SHALL deliver AI responses in real-time using Server-Sent Events (SSE).

#### Scenario: AI typing effect
- **WHEN** AI is processing a request
- **THEN** system SHALL stream the response text character by character
- **AND** display in the chat area as it arrives

#### Scenario: Graph generation notification
- **WHEN** AI decides to generate a graph
- **THEN** system SHALL send intermediate messages like "그래프 생성 중..."
- **AND** stream the final graph configuration

#### Scenario: SSE timeout handling
- **WHEN** SSE connection times out (30 seconds)
- **THEN** system SHALL display a toast error "AI 응답 시간이 초과되었습니다. 다시 시도해주세요"
- **AND** allow user to retry

### Requirement: SQL generation for DuckDB
The system SHALL generate SQL queries that DuckDB can execute to analyze CSV data.

#### Scenario: Generate GROUP BY query
- **WHEN** user requests "지역별 매출"
- **THEN** AI SHALL generate SQL: `SELECT region, SUM(sales) FROM 'data.csv' GROUP BY region`

#### Scenario: Generate time series query
- **WHEN** user requests "월별 추이"
- **THEN** AI SHALL generate SQL with date grouping based on detected date column

#### Scenario: Complex aggregation
- **WHEN** user requests "지역별 월별 매출 heatmap"
- **THEN** AI SHALL generate appropriate pivot-style SQL query

### Requirement: Graph configuration output
The system SHALL output graph configuration in a format that Chart.js can render.

#### Scenario: Line chart configuration
- **WHEN** AI generates a line chart
- **THEN** output SHALL include { type: "line", data: {...}, options: {...} }

#### Scenario: Bar chart configuration
- **WHEN** AI generates a bar chart
- **THEN** output SHALL include { type: "bar", data: {...}, options: {...} }

#### Scenario: Doughnut chart configuration
- **WHEN** AI generates a doughnut chart
- **THEN** output SHALL include { type: "doughnut", data: {...}, options: {...} }

#### Scenario: Scatter chart configuration
- **WHEN** AI generates a scatter chart
- **THEN** output SHALL include { type: "scatter", data: {...}, options: {...} }
