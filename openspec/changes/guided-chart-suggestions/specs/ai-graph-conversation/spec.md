## MODIFIED Requirements

### Requirement: AI 인사이트 추천
CSV 데이터를 분석한 후, 시스템은 AI가 사용자에게 구조화된 차트 추천을 제공하여야 한다.

#### Scenario: 데이터 타입 기반 AI 추천
- **WHEN** 사용자가 차트 관련 질문을 보낼 때
- **THEN** AI는 데이터 구조에 기반한 2~3개의 구체적인 차트 분석 방법을 텍스트로 설명하여야 한다
- **AND** 각 추천에 대해 `[SUGGESTION:{"title":"...", "chart_type":"...", "description":"..."}]` 태그를 응답 텍스트에 포함하여야 한다
- **AND** 사용자가 추천 중 하나를 선택(Action Chip 클릭)하여 차트를 생성할 수 있어야 한다

### Requirement: 실시간 스트리밍 응답
시스템은 Server-Sent Events(SSE)를 사용하여 AI 응답을 실시간으로 전달하여야 한다.

#### Scenario: 그래프 생성 알림
- **WHEN** 사용자가 차트 생성을 유도하는 질문을 보내고 SSE로 채팅 텍스트가 스트리밍될 때
- **THEN** AI는 텍스트 응답에서 분석 방법을 제안하고 구조화된 추천 태그를 포함하여야 한다
- **AND** 프론트엔드는 추천 태그를 파싱하여 Action Chip으로 렌더링하여야 한다
- **AND** 사용자가 Action Chip을 클릭하면 해당 시점에 바구니(Graph Basket)에 placeholder(로딩) 항목을 표시하고 `/api/chart/generate`를 호출하여야 한다
