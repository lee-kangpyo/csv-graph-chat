## Why

현재 사용자가 차트 관련 질문을 하면, 프론트엔드가 자동으로 텍스트 스트리밍(`/api/chat/stream`)과 차트 생성(`/api/chart/generate`)을 동시에 호출한다. 그러나 LLM API의 동시 요청 제한(Rate Limit, 429 에러)으로 인해 병렬 호출이 실패하며, AI가 어떤 차트를 그릴지 사용자에게 선택권이 없어 분석의 정확도와 만족도가 낮다.

이를 **"AI가 분석 방법을 먼저 제안하고, 사용자가 원하는 것을 선택하여 생성하는 가이드형 분석 흐름"**으로 전환한다. Rate Limit 문제를 근본적으로 해결하면서, 사용자 주도의 전문적인 데이터 분석 경험을 제공한다.

## What Changes

- **백엔드**: AI 채팅 응답에 구조화된 차트 추천 리스트를 포함하도록 프롬프트 및 응답 파싱 로직을 개선한다.
- **프론트엔드**: 차트 키워드 감지 시 자동 병렬 호출을 제거한다.
- **프론트엔드**: AI 메시지 내 추천 항목을 클릭 가능한 Action Chip 버튼으로 렌더링하는 UI를 추가한다.
- **프론트엔드**: Action Chip 클릭 시 해당 차트만 `/api/chart/generate`로 생성하고 바스켓에 저장한다.
- **프론트엔드**: "다 그려줘" 등의 일괄 생성 명령을 지원하기 위해 대화 맥락(이전 추천 리스트)을 관리한다.
- **백엔드**: 일괄 생성 요청 시 여러 차트를 순차적으로 생성하는 로직을 추가한다.

## Capabilities

### New Capabilities
- `chart-suggestions`: AI가 사용자 질문에 대해 여러 분석 관점(차트 타입 + 설명)을 구조화된 형태로 제안하는 기능. 프론트엔드에서 Action Chip UI로 렌더링된다.
- `batch-chart-generation`: 사용자가 "다 그려줘" 등 일괄 생성을 요청할 때, 이전 추천 리스트를 기반으로 여러 차트를 순차적으로 생성하는 기능.

### Modified Capabilities
- `ai-chart-generation`: 프론트엔드가 자동 병렬 호출을 하지 않고, 사용자의 명시적 선택(Action Chip 클릭)에 의해서만 `/api/chart/generate`를 호출하도록 호출 트리거를 변경한다.
- `ai-graph-conversation`: 차트 관련 질문 시 AI가 바로 차트를 그리는 대신, 분석 방법을 제안하는 텍스트와 구조화된 추천 리스트를 응답에 포함하도록 프롬프트 계약을 변경한다.

## Impact

- **백엔드**
  - `backend/app/api/insight_recommendation.py`: 차트 추천 리스트를 구조화된 태그로 출력하도록 프롬프트 수정
  - `backend/app/api/chat.py`: SSE 스트리밍 중 추천 태그 파싱 또는 별도 이벤트 전달
  - `backend/app/api/chart.py`: 일괄 생성 엔드포인트 추가 또는 순차 호출 지원

- **프론트엔드**
  - `frontend/src/components/ChatInput.jsx`: 자동 병렬 호출 로직 제거
  - `frontend/src/stores/chatStore.js`: 메시지에 `suggestions` 필드 추가
  - 신규: `frontend/src/components/ActionChips.jsx` (추천 버튼 UI 컴포넌트)
  - AI 메시지 렌더링 컴포넌트: Action Chip을 포함한 메시지 표시

- **테스트**
  - SSE 응답에 추천 태그가 올바르게 포함되는지 검증
  - Action Chip 클릭 시 단일 차트 생성 동작 검증
  - 일괄 생성 시 순차 처리 및 Rate Limit 미발생 검증
