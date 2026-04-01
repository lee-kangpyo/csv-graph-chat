## 1. 유틸리티 통합

- [x] 1.1 `BasketSidebar.jsx`에서 `htmlDownload.js`의 `generateGraphsHTML`과 `downloadHTML` 가져오기
- [x] 1.2 `BasketSidebar.jsx`에서 잘못된 인라인 `generateHTMLDownload` 함수 제거
- [x] 1.3 `handleDownload`를 `downloadHTML(items)` 호출로 업데이트 (수동 blob 생성 대신)

## 2. 검증

- [ ] 2.1 "Download All (HTML)" 버튼 클릭이 HTML 파일 다운로드를 시작하는지 테스트
- [ ] 2.2 다운로드된 HTML 파일을 브라우저에서 열어 그래프가 올바르게 렌더링되는지 확인
- [ ] 2.3 다운로드된 HTML이 Chart.js가 아닌 ECharts를 사용하는지 소스 확인