## MODIFIED Requirements

### Requirement: AI 챗 응답에 차트 설정 포함
#### Scenario: SSE 스트림 응답 형식
- **WHEN** `/api/chat/stream` SSE 엔드포인트가 응답할 때
- **THEN** 각 `message` 이벤트의 데이터는 텍스트 스트리밍 목적의 필드만 포함해야 한다(예: `content`, `request_id`)
- **AND** `message` 이벤트 데이터에 `graph` 필드를 포함해서는 안 된다

#### Scenario: 차트 생성 전용 API 응답 형식
- **WHEN** `POST /api/chart/generate` 엔드포인트가 응답할 때
- **THEN** 응답은 `{"request_id": string, "graph": object | null}` 형식을 따라야 한다
- **AND** `graph`가 필요 없거나 생성 실패 시 `graph: null`을 반환할 수 있다

### Requirement: 프론트엔드 차트 상태 업데이트
#### Scenario: 차트 요청 시 병렬 호출로 graph 수신
- **WHEN** 사용자가 차트 생성을 유도하는 질문을 보낼 때
- **THEN** 프론트엔드는 `/api/chat/stream`(SSE)과 `POST /api/chart/generate`를 동시에 호출해야 한다
- **AND** SSE로 텍스트가 스트리밍되는 동안에도 그래프 생성 요청은 진행 중이어야 한다

#### Scenario: ChatArea에서 SSE graph 이벤트 처리
- **WHEN** SSE 스트림에서 graph 데이터가 포함된 메시지를 수신하면
- **THEN** 프론트엔드는 graph를 SSE로 처리하지 않고(수신하지 않음), 차트 전용 API 응답으로 graph를 처리해야 한다
