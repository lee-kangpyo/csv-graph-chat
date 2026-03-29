## Context

현재 시스템에서 ECharts 차트 렌더링은 `GraphView` 컴포넌트가 담당하며, 백엔드에서 생성된 `graph` 설정 객체를 `echarts.init().setOption()`으로 렌더링한다. 

문제 상황:
- 백엔드에서 생성한 boxplot 설정(dataset transform 방식)이 ECharts에서 렌더링되지 않음
- 매번 전체 플로우(CSV 업로드 → AI 분석 → SSE)를 거쳐야 테스트 가능
- 독립적인 차트 디버깅 환경 부재

## Goals / Non-Goals

**Goals:**
- 백엔드/AI 없이 GraphView에 다양한 ECharts config를 직접 주입하여 렌더링 테스트
- boxplot을 포함한 모든 차트 타입의 preset 제공
- 커스텀 config 입력 기능으로 유연한 디버깅 지원

**Non-Goals:**
- 프로덕션 환경용 UI/UX 개선 (개발용 도구)
- 차트 설정 생성이나 수정 기능
- 백엔드 API 연동

## Decisions

### 1. TestChartPage 독립 라우팅 vs 모달
**결정:** 독립 라우팅 (`/test-chart`)
**이유:** 
- App.jsx에 조건부 렌더링하지 않고 별도 경로로 접근
- 개발 중 자주 열고 닫아도 메인 앱에 영향 없음
- 나중에 프로덕션에서 비활성화하기 쉬움

### 2. Preset Config 구조
**결정:** JavaScript 객체로 preset 정의
```javascript
const presets = {
  bar: { series: [{ type: 'bar', data: [...] }], ... },
  boxplot: { series: [{ type: 'boxplot', data: [[min, Q1, median, Q3, max], ...] }], ... },
  // ...
}
```
**이유:**
- 별도 JSON 파일 없이 소스에 포함
- preset 선택 UI와 동기화 쉬움

### 3. 커스텀 Config 입력
**결정:** Textarea에 JSON 문자열 입력 → JSON.parse → GraphView 전달
**이유:**
- 실제 백엔드 응답을 그대로 붙여넣기 가능
- 설정 수정 후 즉시 결과 확인

## Risks / Trade-offs

- **[Risk]** 잘못된 JSON 입력 시 에러 발생
  - → try-catch로 감싸고 에러 메시지 표시
- **[Risk]** boxplot preset 형식이 올바르지 않을 수 있음
  - → ECharts 공식 문서의 boxplot data 형식([min, Q1, median, Q3, max]) 준수
- **[Trade-off]** 개발용이라 프로덕션 빌드에 포함됨
  - → 향후 Vite 환경에서 개발 모드에서만 로드되도록 설정 가능

## Open Questions

1. 라우팅 라이브러리 사용 여부 (현재 react-router 미사용)
2. preset에 포함할 차트 타입 종류
