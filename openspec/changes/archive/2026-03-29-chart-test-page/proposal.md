## Why

백엔드에서 생성한 ECharts 차트 설정(JSON config)이 실제로 렌더링되는지 테스트하려면 매번 전체 플로우(CSV 업로드 → AI 분석 → SSE 응답)를 거쳐야 한다. 특히 **boxplot** 차트는 ECharts의 dataset transform 방식이 제대로 동작하지 않아 렌더링 실패가 발생하고, 백엔드 없이 독립적으로 디버깅할 방법이 없다.

## What Changes

- **테스트 페이지 컴포넌트 생성** (`TestChartPage.jsx`)
  - GraphView를 사용하여 ECharts config를 렌더링
  - preset 차트 설정들(bar, line, pie, scatter, boxplot 등)을 드롭다운으로 선택
  - 커스텀 config를 입력하여 직접 테스트 가능
  - boxplot 통계값이 series.data에 직접 들어간 올바른 형식도 테스트

- **GraphView 단독 테스트**
  - 백엔드/AI 없이 GraphView가 올바르게 렌더링되는지 확인
  - 다양한 차트 타입(boxplot, sankey, heatmap 등) 검증

## Capabilities

### New Capabilities
- `chart-test-page`: GraphView 기반 테스트 페이지 - 다양한 ECharts preset config를 선택하고 커스텀 config도 입력하여 차트 렌더링을 확인

### Modified Capabilities
- 기존 `chart-rendering` spec의 동작을 검증할 수 있는 테스트 환경 제공 (새로운 요구사항 없음)

## Impact

- **신규 파일**: `frontend/src/components/TestChartPage.jsx`
- **라우팅**: `/test-chart` 경로 추가 (개발용)
- **의존성**: GraphView, echarts (既有)
