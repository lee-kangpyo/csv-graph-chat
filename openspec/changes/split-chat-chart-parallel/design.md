## Context

- 현재 그래프 생성은 `backend/app/api/chat.py`의 `generate_chart_from_file()`에서 수행되며, 채팅 응답 흐름과 결합되어 있다.
- 프론트는 `frontend/src/components/ChatInput.jsx`에서 `POST /api/chat/`로 한 번에 응답을 받는 구조가 기본이다.
- 사용자 목표는 “텍스트 스트리밍 중에도 그래프 생성이 동시에 진행”되고, 그래프가 늦게 와도 사용자가 실패로 오해하지 않게 하는 것이다.

## Goals / Non-Goals

### Goals

- 차트 요청 시 **채팅 SSE**와 **그래프 생성 JSON API**를 병렬로 호출한다.
- 그래프 생성이 완료되기 전에도 바스켓에 **placeholder 로딩 항목**이 표시된다.
- placeholder 상태에서는 BasketItem 클릭으로 GraphModal이 열리지 않는다.
- `request_id`로 동일 사용자 액션(질문 1회)에 대한 응답을 상관시켜, 늦게 도착한 응답이 다른 질문과 섞이지 않게 한다.

### Non-Goals

- 그래프 품질/차트 타입 추천 로직 개선(별도 변경)
- 서버 측 진짜 동시성(스레드/async) 최적화까지 강제(1차는 “프론트 병렬 요청 + 백엔드 API 분리”로 목표 달성)

## Decisions

### 1) API 분리

- `POST /api/chat/stream`
  - 입력: `{ message, csv_metadata, request_id }`
  - 출력: SSE `message` 이벤트에 텍스트 델타(또는 청크)만 포함
  - 종료: `done` 이벤트(텍스트 스트림 종료 신호)

- `POST /api/chart/generate`
  - 입력: `{ message, csv_metadata, request_id }`
  - 출력: `{ request_id, graph }` (graph는 object 또는 null)

### 2) 프론트 병렬 호출

- 차트 요청(키워드/의도)이면:
  - 즉시 바스켓 placeholder 추가(`graph_config: null`, `status: loading`)
  - `createSSEStream` 또는 동등 구현으로 `/api/chat/stream` 시작
  - 동시에 `/api/chart/generate` 시작
- 일반 대화(차트 아님)는 기존처럼 `POST /api/chat/` 유지 가능(범위 최소화)

### 3) 바스켓 placeholder 교체

- placeholder는 `temp-<request_id>` 같은 id로 관리
- chart generate 성공 시:
  - placeholder 제거
  - 기존과 동일하게 `POST /api/basket/`로 저장 후 서버 id로 교체

### 4) 클릭 제한(필수)

- `graph_config`가 없는 BasketItem은 클릭해도 `onGraphClick`을 호출하지 않는다.
- 필요 시 “생성 중” 토스트를 1회만 표시(스팸 방지 정책은 구현 단계에서 조정)

## Risks / Trade-offs

- 요청이 2개로 늘어나 CORS preflight가 추가로 발생할 수 있다(허용 가능한 트레이드오프).
- 동일 질문에 대해 chat/graph 응답 순서가 뒤바뀔 수 있어 `request_id` 상관이 필요하다.
- 백엔드에서 LLM 호출이 동기라도, 프론트 병렬 호출만으로도 사용자 체감은 크게 개선될 수 있다.

## Open Questions

- 차트 요청 판별을 프론트 키워드로 할지, 백엔드에 “의도 분류” 엔드포인트를 둘지(1차는 기존 키워드와 동일 규칙 권장)
