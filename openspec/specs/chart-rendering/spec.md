## ADDED Requirements

### Requirement: ECharts 렌더링
시스템은 CDN에서 로드된 ECharts 라이브러리를 사용하여 차트를 렌더링해야 한다.

#### Scenario: 꺾은선 그래프 렌더링
- **WHEN** AI가 꺾은선 그래프 설정을 생성하면
- **THEN** 시스템은 type이 "line"인 ECharts로 렌더링해야 한다
- **AND** 그래프 영역에 표시해야 한다

#### Scenario: 막대 그래프 렌더링
- **WHEN** AI가 막대 그래프 설정을 생성하면
- **THEN** 시스템은 type이 "bar"인 ECharts로 렌더링해야 한다

#### Scenario: 파이 차트 렌더링
- **WHEN** AI가 파이 차트 설정을 생성하면
- **THEN** 시스템은 type이 "pie"인 ECharts로 렌더링해야 한다

#### Scenario: 산점도 렌더링
- **WHEN** AI가 산점도 설정을 생성하면
- **THEN** 시스템은 type이 "scatter"인 ECharts로 렌더링해야 한다

#### Scenario: 히트맵 렌더링
- **WHEN** AI가 히트맵 설정을 생성하면
- **THEN** 시스템은 type이 "heatmap"인 ECharts로 렌더링해야 한다
- **AND** 날짜 기반 히트맵(월별, 분기별)을 지원해야 한다

#### Scenario: 산키 다이어그램 렌더링
- **WHEN** AI가 산키 다이어그램 설정을 생성하면
- **THEN** 시스템은 type이 "sankey"인 ECharts로 렌더링해야 한다

#### Scenario: 선버스트 차트 렌더링
- **WHEN** AI가 선버스트 차트 설정을 생성하면
- **THEN** 시스템은 type이 "sunburst"인 ECharts로 렌더링해야 한다

### Requirement: 실시간 차트 업데이트
시스템은 AI가 수정된 설정을 보내면 실시간으로 차트를 업데이트해야 한다.

#### Scenario: 대화 중 차트 업데이트
- **WHEN** 사용자가 수정을 요청하면
- **THEN** 시스템은 페이지 새로고침 없이 차트를 업데이트해야 한다
- **AND** 부드러운 전환을 유지해야 한다

### Requirement: 차트 반응형 크기 조정
시스템은 컨테이너 크기에 따라 차트가 반응하도록 해야 한다.

#### Scenario: 반응형 차트
- **WHEN** 차트 컨테이너 크기가 변경되면(창 크기 조정, 사이드바 토글)
- **THEN** 차트는 자동으로 컨테이너에 맞게 조정되어야 한다
- **AND** 종횡비를 유지해야 한다

### Requirement: AI가 생성한 ECharts 설정 수락
시스템은 AI가 생성한 ECharts 설정 객체를 받아들여야 MUST 한다.

#### Scenario: 완전한 ECharts 설정 수락
- **WHEN** AI가 { series: [{ type, data, ... }], xAxis, yAxis, ... }形式的 설정을 보내면
- **THEN** 시스템은 이를 echarts.init(dom).setOption(config)로 직접 전달해야 한다

#### Scenario: 옵션 누락 시
- **WHEN** AI가 옵션 없이 설정을 보내면
- **THEN** 시스템은 반응형과 툴팁을 위한 기본 옵션을 적용해야 한다

### Requirement: HTML로 차트 다운로드
시스템은 차트를 독립형 HTML 파일로 내보낼 수 있어야 한다.

#### Scenario: HTML 내보내기에 데이터 포함
- **WHEN** 사용자가 차트를 HTML로 다운로드하면
- **THEN** HTML은 다음을 포함해야 한다:
- **AND** CDN의 ECharts
- **AND** 임베디드 차트 설정
- **AND** 임베디드 데이터 값(외부 참조 없이)

#### Scenario: 오프라인에서 HTML 뷰어
- **WHEN** 사용자가 인터넷 없이 다운로드된 HTML 파일을 열면
- **THEN** CDN이 캐시된 경우 차트가 올바르게 렌더링되어야 한다
