## Why

TestChartPage의 차트 선택 옵션이 7개(bar, line, pie, scatter, boxplot, heatmap, sankey)로 제한되어 있어 ECharts가 지원하는 다양한 차트 유형을 테스트할 수 없다. 사용자가 더 다양한 데이터 시각화 시나리오를 테스트할 수 있도록 차트 유형을 확장해야 한다.

## What Changes

- TestChartPage에 12개 이상의 새 차트 유형 추가 (Radar, Polar, Graph, Tree, Sunburst, Treemap, Parallel, Gauge, Funnel, Candlestick, ThemeRiver, Calendar)
- 각 차트 유형에 적합한 샘플 데이터와 설정 포함
- 기존 7개 차트-preset 유지

## Capabilities

### New Capabilities
- `echarts-chart-types`: ECharts支持的全图表类型测试页面，包含每种图表类型的预设配置和示例数据

## Impact

- 수정 파일: `frontend/src/components/TestChartPage.jsx`
- 의존성: ECharts 라이브러리 (기존 사용 중)