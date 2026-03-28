## MODIFIED Requirements

### Requirement: AI가 생성한 ECharts 설정 수락
시스템은 AI가 생성한 ECharts 설정 객체를 받아들여야 MUST 한다.

#### Scenario: 완전한 ECharts 설정 수락
- **WHEN** AI가 { series: [{ type, data, ... }], xAxis, yAxis, ... }形式的 설정을 보내면
- **THEN** 시스템은 이를 echarts.init(dom).setOption(config)로 직접 전달해야 한다

#### Scenario: 옵션 누락 시
- **WHEN** AI가 옵션 없이 설정을 보내면
- **THEN** 시스템은 반응형과 툴팁을 위한 기본 옵션을 적용해야 한다

#### Scenario: 백엔드 API 응답에서 차트 설정 수락
- **WHEN** 백엔드 API가 `{"content": "...", "graph": {...}}`形式 응답을 반환하면
- **THEN** 프론트엔드는 `graph` 필드를 추출하여 차트로 렌더링해야 한다

#### Scenario: SSE 스트림에서 차트 설정 수락
- **WHEN** SSE 스트림 이벤트가 `{"content": "...", "graph": {...}}`形式 데이터를 포함하면
- **THEN** 프론트엔드는 실시간으로 차트를 업데이트해야 한다
