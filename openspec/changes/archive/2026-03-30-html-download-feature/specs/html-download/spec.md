## ADDED Requirements

### Requirement: HTML 다운로드
시스템은 사용자가 ECharts를 사용하여 올바르게 렌더링되는 독립 실행형 HTML 파일로 차트 데이터를 다운로드할 수 있어야 한다.

#### Scenario: 단일 그래프 HTML 다운로드
- **WHEN** 사용자가 그래프를 선택하고 HTML 다운로드 버튼을 클릭하면
- **THEN** 시스템은 ECharts로 그래프를 렌더링하는 HTML 파일을 생성해야 한다
- **AND** 파일이 사용자의 디바이스로 다운로드된다

#### Scenario: 다운로드된 HTML이 자체 포함됨
- **WHEN** 사용자가 다운로드된 HTML 파일을 브라우저에서 열면
- **THEN** 외부 서버나 네트워크 요청 없이 그래프가 렌더링된다
- **AND** ECharts가 HTML 파일 내 CDN에서 로드된다

### Requirement: 콘텐츠 보안
시스템은 XSS 공격을 방지하기 위해 다운로드된 HTML 파일에서 모든 사용자 제공 콘텐츠를 이스케이프해야 한다.

#### Scenario: 그래프 이름 이스케이프
- **WHEN** HTML 특수 문자가 포함된 이름의 그래프를 다운로드하면
- **THEN** 특수 문자가 HTML 출력에서 올바르게 이스케이프된다
- **AND** 그래프 제목이 스크립트 실행 없이 올바르게 표시된다