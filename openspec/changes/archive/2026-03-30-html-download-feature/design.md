## Context

HTML 다운로드 기능은 차트 데이터를 독립 실행형 HTML 파일로 내보낼 수 있어야 한다. 애플리케이션은 ECharts를 사용하여 차트 렌더링을 수행하며, `frontend/src/utils/htmlDownload.js`에 올바른 유틸리티가 존재한다:
- ECharts를 CDN에서 로드
- `echarts.init()`으로 차트 초기화
- `chart.setOption()`으로 옵션 설정
- HTML 콘텐츠 이스케이프

그러나 `BasketSidebar.jsx`에는 다음과 같은 자체 인라인 `generateHTMLDownload()` 함수가 있다:
- Chart.js CDN 대신 ECharts 사용
- ECharts 설정과 함께 Chart.js API (`new Chart(canvas, config)`) 사용
- `graph.name` 이스케이프 안 함 (XSS 취약점)

## Goals / Non-Goals

**Goals:**
- 잘못된 인라인 HTML 다운로드를 올바른 유틸리티로 교체
- 다운로드된 HTML 파일이 ECharts 그래프를 올바르게 렌더링하도록 보장
- 그래프 이름 처리에서 XSS 취약점 수정

**Non-Goals:**
- `htmlDownload.js` 유틸리티 자체 수정 (이미 올바르게 작동함)
- 새 다운로드 형식 또는 옵션 추가

## Decisions

### 1. 기존 유틸리티 가져오기

**선택**: 이미 ECharts를 사용하여 올바르게 구현된 `htmlDownload.js` 유틸리티를 가져와서 사용

**이유**: 
- 유틸리티가 이미 존재하고 테스트됨
- Chart.js가 아닌 ECharts 사용
- `escapeHTML()` 함수가 이미 정의됨

### 2. 데이터 구조 호환성

**선택**: 컴포넌트에서 전달되는 `graph_config`가 유틸리티의 예상 구조와 일치하는지 확인

**이유**: 
- `BasketSidebar.jsx`의 `items` 배열이 `graph.graph_config` 형태의 설정을 가지고 있으므로 유틸리티와 호환 가능

## Risks / Trade-offs

- [Risk] `graph_config` 구조가 유틸리티 예상과 다를 경우
  - → Mitigation: 구현 전에 데이터 구조 확인
- [보안] 이스케이프되지 않은 `graph.name`으로 인한 XSS
  - → Mitigation: 유틸리티의 `escapeHTML()` 함수를 사용하면 해결됨 (인라인 코드에서는 사용되지 않던 함수)