## ADDED Requirements

### Requirement: AI 챗 응답에 차트 설정 포함
백엔드는 AI 대화 응답에 ECharts 차트 설정을 포함 MUST 한다.

#### Scenario: POST API 응답 형식
- **WHEN** `/api/chat/` POST 엔드포인트가 응답할 때
- **THEN** 응답은 `{"content": string, "graph": object | null}`形式을 MUST 따라야 한다
- **AND** graph가 필요 없으면 `graph: null`을 반환할 수 있다

#### Scenario: SSE 스트림 응답 형식
- **WHEN** `/api/chat/stream` SSE 엔드포인트가 응답할 때
- **THEN** 각 `message` 이벤트의 데이터는 `{"content": string, "graph": object | null}`形式을 MUST 포함할 수 있다

### Requirement: 프론트엔드 차트 상태 업데이트
프론트엔트는 MUST API 응답에서 차트 설정을 추출하여 렌더링해야 한다.

#### Scenario: ChatInput에서 onGraphGenerated 호출
- **WHEN** `/api/chat/` POST 요청이 `graph` 필드와 함께 응답하면
- **THEN** ChatInput 컴포넌트는 `onGraphGenerated(graph)` 콜백을 MUST 호출해야 한다

#### Scenario: ChatArea에서 SSE graph 이벤트 처리
- **WHEN** SSE 스트림에서 graph 데이터가 포함된 메시지를 수신하면
- **THEN** ChatArea 컴포넌트는 그래프 영역을 MUST 업데이트해야 한다

### Requirement: 차트 설정 유효성 검증
프론트엔트는 MUST 수신된 차트 설정의 유효성을 검증해야 한다.

#### Scenario: 유효하지 않은 graph 데이터 무시
- **WHEN** `graph` 필드가 null이거나 유효한 object가 아니면
- **THEN** 시스템은 차트 렌더링을 시도하지 않고 해당 필드를 MUST 무시해야 한다
