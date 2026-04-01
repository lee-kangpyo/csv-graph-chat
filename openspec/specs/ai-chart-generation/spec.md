## Purpose
AI 대화 응답에 ECharts 차트 설정을 포함하여 프론트엔드에서 렌더링하는 종단 간 차트 생성 플로우

## Requirements

### Requirement: AI 챗 응답에 차트 설정 포함
백엔드는 AI 대화 응답에 ECharts 차트 설정을 포함해야 한다.

#### Scenario: POST API 응답 형식
- **WHEN** `/api/chat/` POST 엔드포인트가 응답할 때
- **THEN** 응답은 `{"content": string, "graph": object | null}` 형식을 따라야 한다
- **AND** graph가 필요 없으면 `graph: null`을 반환할 수 있다

#### Scenario: SSE 스트림 응답 형식
- **WHEN** `/api/chat/stream` SSE 엔드포인트가 응답할 때
- **THEN** 각 `message` 이벤트의 데이터는 텍스트 스트리밍 목적의 필드만 포함해야 한다(예: `content`, `request_id`)
- **AND** `message` 이벤트 데이터에 `graph` 필드를 포함해서는 안 된다

#### Scenario: 차트 생성 전용 API 응답 형식
- **WHEN** `POST /api/chart/generate` 엔드포인트가 응답할 때
- **THEN** 응답은 `{"request_id": string, "graph": object | null}` 형식을 따라야 한다
- **AND** `graph`가 필요 없거나 생성 실패 시 `graph: null`을 반환할 수 있다

#### Scenario: 실제 데이터 기반 차트 생성
- **WHEN** 백엔드가 차트 생성 요청을 처리할 때
- **THEN** 시스템은 더미 데이터가 아닌 pandas로 처리한 실제 CSV 데이터를 chart config에 사용해야 한다
- **AND** LLM이 결정한 분석 intent(group_by, time_series 등)를 기반으로 데이터를 처리해야 한다

### Requirement: 프론트엔드 차트 상태 업데이트
프론트엔드는 API 응답에서 차트 설정을 추출하여 렌더링해야 한다.

#### Scenario: 차트 요청 시 병렬 호출로 graph 수신
- **WHEN** 사용자가 차트 생성을 유도하는 질문을 보낼 때
- **THEN** 프론트엔드는 `/api/chat/stream`(SSE)과 `POST /api/chart/generate`를 동시에 호출해야 한다
- **AND** SSE로 텍스트가 스트리밍되는 동안에도 그래프 생성 요청은 진행 중이어야 한다

#### Scenario: ChatArea에서 SSE graph 이벤트 처리
- **WHEN** SSE 스트림에서 graph 데이터가 포함된 메시지를 수신하면
- **THEN** 프론트엔드는 graph를 SSE로 처리하지 않고(수신하지 않음), 차트 전용 API 응답으로 graph를 처리해야 한다

### Requirement: 차트 설정 유효성 검증
프론트엔드는 수신된 차트 설정의 유효성을 검증해야 한다.

#### Scenario: 유효하지 않은 graph 데이터 무시
- **WHEN** `graph` 필드가 null이거나 유효한 object가 아니면
- **THEN** 시스템은 차트 렌더링을 시도하지 않고 해당 필드를 무시해야 한다
