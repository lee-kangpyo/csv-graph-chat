## Why

HTML 다운로드 기능이 Chart.js API를 사용하여 ECharts 설정으로 렌더링하려고 시도하고 있어 다운로드된 HTML 파일이 차트를 올바르게 렌더링하지 못한다. 올바른 `htmlDownload.js` 유틸리티가 존재하지만 `BasketSidebar.jsx`에서 통합되지 않았다.

## What Changes

- `BasketSidebar.jsx`의 잘못된 인라인 `generateHTMLDownload()` 함수를 기존 `htmlDownload.js` 유틸리티로 교체
- UI에서 다운로드 트리거를 실행하도록 올바르게 통합
- 그래프 이름의 XSS 취약점 수정
- 다운로드된 HTML이 ECharts 기반 그래프를 올바르게 렌더링하도록 보장

## Capabilities

### New Capabilities

- `html-download`: ECharts로 올바르게 렌더링되는 독립 실행형 HTML 파일로 차트 데이터를 내보내기

### Modified Capabilities

- 없음

## Impact

- **프론트엔드**: `BasketSidebar.jsx` - 인라인 `generateHTMLDownload()`를 `htmlDownload.js` 가져오기 및 사용으로 교체
- **프론트엔드**: `htmlDownload.js` 유틸리티가 존재하며 올바르게 구현됨
- **보안**: 그래프 이름 처리에서 XSS 취약점 수정