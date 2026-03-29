## MODIFIED Requirements

### Requirement: AI 챗 응답에 차트 설정 포함
백엔드는 AI 대화 응답에 ECharts 차트 설정을 포함해야 한다.

#### Scenario: 실제 데이터 기반 차트 생성
- **WHEN** 백엔드가 차트 생성 요청을 처리할 때
- **THEN** 시스템은 더미 데이터가 아닌 pandas로 처리한 실제 CSV 데이터를 chart config에 사용해야 한다
- **AND** LLM이 결정한 분석 intent(group_by, time_series 등)를 기반으로 데이터를 처리해야 한다
