## ADDED Requirements

### Requirement: Preset Chart Selection
테스트 페이지는 predefined preset 차트 설정들을 드롭다운으로 선택할 수 있어야 한다.

#### Scenario: Bar chart preset selection
- **WHEN** 사용자가 "Bar Chart" preset을 선택하면
- **THEN** GraphView에 bar chart config가 전달되어 렌더링된다

#### Scenario: Boxplot preset selection
- **WHEN** 사용자가 "Boxplot" preset을 선택하면
- **THEN** GraphView에 boxplot config (series.data: [[min, Q1, median, Q3, max], ...])가 전달되어 렌더링된다

#### Scenario: Multiple chart type presets
- **WHEN** 사용자가 preset 목록을 확인하면
- **THEN** bar, line, pie, scatter, boxplot, heatmap, sankey 타입의 preset이 표시된다

### Requirement: Custom Config Input
테스트 페이지는 사용자가 직접 JSON config를 입력할 수 있어야 한다.

#### Scenario: Valid custom JSON input
- **WHEN** 사용자가 유효한 JSON config를 textarea에 입력하고 "Apply"를 클릭하면
- **THEN** GraphView에 해당 config가 전달되어 렌더링된다

#### Scenario: Invalid JSON input
- **WHEN** 사용자가 유효하지 않은 JSON을 입력하고 "Apply"를 클릭하면
- **THEN** 에러 메시지가 표시되며 기존 렌더링은 유지된다

### Requirement: GraphView Rendering
테스트 페이지는 GraphView 컴포넌트를 사용하여 ECharts 차트를 렌더링해야 한다.

#### Scenario: GraphView receives config prop
- **WHEN** preset이 선택되거나 커스텀 config가 적용되면
- **THEN** GraphView의 config prop이 업데이트되어 차트가 다시 렌더링된다

#### Scenario: Chart cleanup on unmount
- **WHEN** 테스트 페이지가 언마운트되면
- **THEN** ECharts 인스턴스가 dispose되어 메모리 누수가 방지된다
