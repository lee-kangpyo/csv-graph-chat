## Purpose

AI가 사용자 질문에 대해 여러 분석 관점(차트 타입 + 설명)을 구조화된 형태로 제안하는 기능. 프론트엔드에서 Action Chip UI로 렌더링된다.

## Requirements

### Requirement: 구조화된 차트 추천 생성
AI는 차트 관련 질문에 대해 2~3개의 구조화된 차트 추천을 응답 텍스트에 포함하여야 한다.

#### Scenario: 차트 추천 태그 출력
- **WHEN** 사용자가 차트 생성을 유도하는 질문을 보낼 때
- **THEN** AI 응답 텍스트 끝에 `[SUGGESTION:{"title":"...", "chart_type":"...", "description":"..."}]` 형태의 구조화된 태그가 2~3개 포함되어야 한다
- **AND** 각 추천 항목의 `title`은 한글이어야 한다
- **AND** `chart_type`은 시스템이 지원하는 11종 차트 타입 중 하나여야 한다
- **AND** `description`은 해당 분석이 데이터에서 어떤 인사이트를 줄 수 있는지 1문장으로 설명해야 한다

#### Scenario: 일반 대화에서는 추천 미포함
- **WHEN** 사용자가 차트와 무관한 일반 대화를 보낼 때
- **THEN** AI 응답에 `[SUGGESTION:...]` 태그가 포함되지 않아야 한다

### Requirement: 추천 항목 프론트엔드 파싱
프론트엔드는 SSE 스트리밍 중 추천 태그를 실시간으로 파싱하여 UI에 반영하여야 한다.

#### Scenario: SSE 스트리밍 중 추천 태그 파싱
- **WHEN** SSE 텍스트 청크에 `[SUGGESTION:` 패턴이 감지될 때
- **THEN** 프론트엔드는 `]`가 닫힐 때까지 버퍼링하여야 한다
- **AND** 완전한 태그가 수신되면 JSON을 파싱하여 `suggestions` 배열에 추가하여야 한다
- **AND** 파싱된 태그는 채팅 텍스트에 표시하지 않고 제거하여야 한다

#### Scenario: 추천 태그 파싱 실패 시 graceful 처리
- **WHEN** `[SUGGESTION:...]` 태그의 JSON이 유효하지 않을 때
- **THEN** 해당 태그는 무시하고 텍스트 응답은 정상 표시하여야 한다
- **AND** 다른 유효한 추천 항목은 영향받지 않아야 한다

### Requirement: Action Chip UI 렌더링
프론트엔드는 AI 메시지에 포함된 추천 항목을 클릭 가능한 버튼(Action Chip) 형태로 렌더링하여야 한다.

#### Scenario: AI 메시지 하단에 Action Chip 표시
- **WHEN** AI 메시지에 1개 이상의 추천 항목(`suggestions`)이 있을 때
- **THEN** 메시지 텍스트 하단에 각 추천 항목이 클릭 가능한 Action Chip 버튼으로 표시되어야 한다
- **AND** 각 Chip에는 추천 `title`과 `chart_type` 아이콘/라벨이 포함되어야 한다
- **AND** Chip에 마우스를 올리면 `description`이 툴팁으로 표시되어야 한다

#### Scenario: Action Chip 클릭으로 단일 차트 생성
- **WHEN** 사용자가 Action Chip 버튼을 클릭할 때
- **THEN** 해당 추천 항목의 정보와 원본 질문을 기반으로 `/api/chart/generate`를 호출하여야 한다
- **AND** 바구켓에 로딩 placeholder를 즉시 추가하여야 한다
- **AND** 차트 생성 성공 시 placeholder를 실제 차트로 교체하고 `POST /api/basket/`로 저장하여야 한다
- **AND** 클릭된 Chip은 비활성화 상태(이미 생성됨)로 변경되어야 한다

#### Scenario: 추천이 없는 AI 메시지
- **WHEN** AI 메시지에 추천 항목이 없을 때
- **THEN** Action Chip 영역은 렌더링되지 않아야 한다
