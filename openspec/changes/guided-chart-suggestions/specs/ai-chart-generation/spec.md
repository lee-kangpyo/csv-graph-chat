## MODIFIED Requirements

### Requirement: 프론트엔드 차트 상태 업데이트
프론트엔드는 API 응답에서 차트 설정을 추출하여 렌더링하여야 한다.

#### Scenario: 차트 요청 시 사용자 선택에 의한 graph 생성
- **WHEN** 사용자가 차트 생성을 유도하는 질문을 보낼 때
- **THEN** 프론트엔드는 `/api/chat/stream`(SSE)만 호출하여 텍스트를 스트리밍하여야 한다
- **AND** `/api/chart/generate`를 자동으로 동시 호출하지 않아야 한다
- **AND** AI 응답에 포함된 추천 항목(Action Chip)을 사용자가 클릭할 때에만 `/api/chart/generate`를 호출하여야 한다

#### Scenario: ChatArea에서 SSE graph 이벤트 처리
- **WHEN** SSE 스트림에서 graph 데이터가 포함된 메시지를 수신하면
- **THEN** 프론트엔드는 graph를 SSE로 처리하지 않고(수신하지 않음), 차트 전용 API 응답으로 graph를 처리하여야 한다
