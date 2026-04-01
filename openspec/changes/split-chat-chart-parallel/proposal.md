## Why

현재 채팅 응답(`POST /api/chat/`)과 그래프 생성이 한 요청 흐름에 묶이면, 사용자는 텍스트는 먼저 끝난 것처럼 보이는데 그래프는 한참 뒤에 도착해 “그래프가 안 그려졌다”고 오해할 수 있다.

사용자는 **텍스트 스트리밍이 진행되는 동안 그래프 생성(2번째 처리)도 동시에 진행**되길 원하며, 그래프가 준비되기 전에도 **바스켓에 로딩(placeholder) 항목이 먼저 표시**되길 원한다.

## What Changes

- **백엔드**: 채팅(SSE)과 그래프 생성(JSON) API를 분리한다.
  - `POST /api/chat/stream`: 텍스트만 SSE로 스트리밍한다(그래프 생성은 포함하지 않음).
  - `POST /api/chart/generate`: 그래프(ECharts `graph_config`)만 JSON으로 생성한다.

- **프론트엔드**: 차트 요청이 감지되면 다음을 **동시에** 수행한다.
  - SSE로 채팅 텍스트를 스트리밍한다.
  - 동시에 `/api/chart/generate`를 호출한다.
  - 그래프 생성 전 바스켓에 **placeholder(로딩) 항목**을 먼저 추가하고, 완료 시 기존 `POST /api/basket/` 자동 저장 흐름으로 최종 항목으로 교체한다.

- **UX**: placeholder(로딩) 상태의 BasketItem은 클릭으로 모달을 열 수 없어야 한다(빈 모달/배경 잠금 등 UX 버그 방지).

## Capabilities

### Modified Capabilities

- `ai-graph-conversation`: SSE는 텍스트 스트리밍만 담당하도록 계약을 정리한다.
- `ai-chart-generation`: 그래프 생성은 전용 엔드포인트로 분리하고 프론트가 병렬 호출하도록 시나리오를 확장한다.
- `auto-basket-save`: 그래프 생성 대기 구간의 낙관적 바스켓 갱신(placeholder 로딩) 시나리오를 추가한다.
- `graph-basket-preview`: 로딩 placeholder에서는 미리보기/클릭 동작을 제한한다.
- `graph-modal-viewing`: `graph_config`가 없는 항목은 모달이 열리지 않아야 한다.

## Impact

- **백엔드**
  - `backend/app/api/chat.py`: `/api/chat/stream`에서 graph 생성 제거(텍스트 전용)
  - `backend/app/main.py`: 새 라우터 등록(예: `chart_router`)
  - 신규: `backend/app/api/chart.py` (또는 동등 모듈)에 `POST /api/chart/generate`

- **프론트엔드**
  - `frontend/src/components/ChatInput.jsx`: 차트 요청 시 SSE + chart generate 병렬 호출, placeholder 바스켓 추가/교체
  - `frontend/src/components/BasketItem.jsx`: 로딩 상태 클릭 제한(및 시각적 로딩 표시)
  - `frontend/src/App.jsx`(필요 시): 모달 오픈 가드

- **테스트**
  - `backend/tests/test_chart_rendering_spec.py`: SSE가 graph를 포함하지 않는지, chart generate가 graph를 반환하는지 등 계약 테스트 갱신
