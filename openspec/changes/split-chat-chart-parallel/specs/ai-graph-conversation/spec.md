## MODIFIED Requirements

### Requirement: 실시간 스트리밍 응답
#### Scenario: 그래프 생성 알림
- **WHEN** 사용자가 차트 생성을 유도하는 질문을 보내고 SSE로 채팅 텍스트가 스트리밍될 때
- **THEN** 프론트엔드는 그래프 생성이 진행 중임을 사용자에게 명확히 보여줘야 한다
- **AND** 바구니(Graph Basket)에 placeholder(로딩) 항목을 즉시 표시하거나 동등한 로딩 UI를 제공해야 한다
- **AND** 최종 그래프 설정은 `POST /api/chart/generate` 응답으로 수신되어야 한다
