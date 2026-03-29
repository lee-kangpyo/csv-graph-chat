## 1. Project Setup

- [x] 1.1 Create TestChartPage.jsx component file in frontend/src/components/
- [x] 1.2 Import GraphView and echarts dependencies

## 2. Preset Config Definitions

- [x] 2.1 Define bar chart preset config
- [x] 2.2 Define line chart preset config
- [x] 2.3 Define pie chart preset config
- [x] 2.4 Define scatter chart preset config
- [x] 2.5 Define boxplot preset config (with correct series.data format: [[min, Q1, median, Q3, max], ...])
- [x] 2.6 Define heatmap preset config
- [x] 2.7 Define sankey preset config

## 3. UI Components

- [x] 3.1 Create preset selector dropdown (select element)
- [x] 3.2 Create custom config textarea input
- [x] 3.3 Create "Apply" button for custom config
- [x] 3.4 Create error display for invalid JSON input

## 4. State Management

- [x] 4.1 Manage selected preset state
- [x] 4.2 Manage custom config input state
- [x] 4.3 Handle config application logic (preset selection vs custom input)

## 5. Integration & Routing

- [x] 5.1 Add /test-chart route to App.jsx (conditionally, dev mode)
- [x] 5.2 Connect preset selection to GraphView rendering
- [x] 5.3 Connect custom config input to GraphView rendering

## 6. Testing (Manual)

- [ ] 6.1 Test bar chart preset renders correctly
- [ ] 6.2 Test boxplot preset renders correctly (verify series.data format works)
- [ ] 6.3 Test custom JSON input handles valid config
- [ ] 6.4 Test custom JSON input handles invalid JSON gracefully
