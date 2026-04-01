## Context

TestChartPage (`frontend/src/components/TestChartPage.jsx`)는 ECharts 차트 라이브러리를 사용하여 다양한 차트 유형을 테스트하는 페이지이다. 현재 7개의 차트 유형(bar, line, pie, scatter, boxplot, heatmap, sankey)만 제공한다.

## Goals / Non-Goals

**Goals:**
- ECharts 지원 차트 유형 중 유용한 12개 이상 추가
- 각 차트에 적합한 샘플 데이터 포함
- 기존 select UI 확장

**Non-Goals:**
- 새로운 컴포넌트 생성 없음 (기존 구조 활용)
- 차트 렌더링 로직 수정 없음

## Decisions

1. **새 차트 유형**: radar, polar, graph, tree, sunburst, treemap, parallel, gauge, funnel, candlestick, themeriver, calendar
2. **샘플 데이터**: 각 차트에 현실적인 예시 데이터 포함 (금융, 학생 데이터 등)
3. **UI 변경**: select dropdown에 새 옵션 추가만 수행

## Risks / Trade-offs

- 차트 유형이 늘어나면 select 목록이 길어짐 → 카테고리分组은 향후 고려
