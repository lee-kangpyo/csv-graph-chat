## Why

사용자와 AI가 대화를 통해 데이터를 분석할 때, AI가 생성한 차트 설정(ECharts config)이 실제로 렌더링되지 않는 문제가 있다. 프론트엔드에 ECharts와 차트 렌더링 인프라(GraphView, graphStore)가 이미 구축되어 있지만, 백엔드 API 응답과 프론트엔드 메시지 처리 로직에서 차트 설정을 전달하는 부분이 구현되어 있지 않다.

## What Changes

- **백엔드**: `/api/chat/` POST 엔드포인트가 대화 내용과 함께 ECharts 차트 설정(`graph` 필드)을 응답에 포함
- **프론트엔드**: API 응답에서 `graph` 필드를 추출하여 `onGraphGenerated` 콜백 호출
- **프론트엔드**: SSE 스트림 응답 처리 시에도 차트 설정 지원 (`/api/chat/stream`)

## Capabilities

### New Capabilities

- `ai-chart-generation`: AI가 대화에 기반하여 ECharts 차트 설정을 생성하고, 프론트엔드가 이를 렌더링하는 종단 간 플로우
  - 백엔드: LLM 응답에서 차트 생성 요청 감지 → ECharts config 생성 → API 응답에 포함
  - 프론트엔드: API 응답의 graph 필드 파싱 → graphStore 업데이트 → GraphView 렌더링

### Modified Capabilities

- `chart-rendering`: 기존 chart-rendering 스펙의 "AI가 생성한 ECharts 설정 수락" 시나리오가 실제로 동작하도록 구현 활성화

## Impact

- **백엔드**: `app/api/chat.py` - 응답 포맷 변경 (`content` → `content` + `graph`)
- **백엔드**: `app/api/llm_client.py` 또는 새 모듈 - LLM 응답에서 차트 설정 추출/생성 로직
- **프론트엔드**: `ChatInput.jsx` - `onGraphGenerated` 콜백 호출 로직 추가
- **프론트엔드**: `ChatArea.jsx` - SSE 스트림에서 graph 이벤트 처리 고려
