## 1. 백엔드: 추천 프롬프트 개선

- [x] 1.1 `backend/app/api/insight_recommendation.py`의 `generate_insight_prompt()`를 수정하여, 차트 관련 질문 시 AI가 응답 끝에 `[SUGGESTION:{"title":"...", "chart_type":"...", "description":"..."}]` 태그를 2~3개 포함하도록 프롬프트를 강화한다
- [x] 1.2 일반 대화(차트 무관)에서는 추천 태그를 포함하지 않도록 프롬프트에 조건을 명시한다

## 2. 백엔드: async def → def 변환 (서버 안정성)

- [x] 2.1 `backend/app/api/chat.py`의 `chat_stream`, `chat` 엔드포인트를 `def`(동기)로 변경하여 동기 LLM 호출이 이벤트 루프를 블로킹하지 않도록 한다
- [x] 2.2 `backend/app/api/chart.py`의 `generate_chart` 엔드포인트를 `def`(동기)로 변경한다
- [x] 2.3 `backend/app/api/llm_client.py`의 `OpenAI` 클라이언트에 `max_retries=5`를 추가하여 간헐적 429 에러에 대한 자동 재시도를 설정한다

## 3. 프론트엔드: 자동 병렬 호출 제거

- [x] 3.1 `frontend/src/components/ChatInput.jsx`에서 `detectChartRequest()` 기반 자동 `/api/chart/generate` 호출 로직을 제거한다
- [x] 3.2 `CHART_KEYWORDS` 기반 자동 placeholder 추가 로직을 제거한다
- [x] 3.3 차트 관련 질문이든 일반 질문이든 `/api/chat/stream` SSE만 호출하도록 통합한다

## 4. 프론트엔드: chatStore 확장

- [x] 4.1 `frontend/src/stores/chatStore.js`의 메시지 구조에 `suggestions` 배열 필드를 추가한다 (`{ role, content, timestamp, suggestions }`)
- [x] 4.2 `addMessage` 함수에 `suggestions` 파라미터를 추가한다

## 5. 프론트엔드: SSE 추천 태그 파싱

- [x] 5.1 `ChatInput.jsx`의 SSE 수신 로직에 `[SUGGESTION:...]` 태그 버퍼 파싱 로직을 추가한다
- [x] 5.2 파싱된 추천 태그는 화면 텍스트에서 제거하고 `suggestions` 배열에 누적한다
- [x] 5.3 SSE `done` 이벤트 시 누적된 `suggestions`를 해당 AI 메시지에 저장한다
- [x] 5.4 파싱 실패 시 해당 태그를 무시하고 텍스트 응답을 정상 표시한다

## 6. 프론트엔드: Action Chip UI 컴포넌트

- [x] 6.1 `frontend/src/components/ActionChips.jsx` 신규 컴포넌트를 생성한다 (추천 항목을 클릭 가능한 Chip 버튼으로 렌더링)
- [x] 6.2 각 Chip에 `title`, `chart_type` 라벨을 표시하고, 마우스 hover 시 `description` 툴팁을 표시한다
- [x] 6.3 Chip 클릭 시 `/api/chart/generate`를 호출하고 바스켓에 placeholder를 추가하는 핸들러를 구현한다
- [x] 6.4 이미 생성된 Chip은 비활성화 상태로 변경한다
- [x] 6.5 AI 메시지 렌더링 영역에 ActionChips 컴포넌트를 통합한다

## 7. 프론트엔드: "다 그려줘" 일괄 생성

- [x] 7.1 일괄 생성 키워드 리스트(`BATCH_KEYWORDS`)를 정의한다 ("다 그려", "전부 그려", "모두 그려", "다 만들어", "전부 만들어")
- [x] 7.2 사용자 메시지가 일괄 키워드를 포함하고 직전 AI 메시지에 `suggestions`가 있으면, 일괄 생성 모드로 진입한다
- [x] 7.3 `suggestions` 배열을 순회하며 `/api/chart/generate`를 하나씩 `await`로 호출한다 (순차 처리)
- [x] 7.4 각 차트 완료 시마다 바스켓에 즉시 반영하고 진행 상황("2/3 차트 생성 중...")을 표시한다
- [x] 7.5 개별 차트 생성 실패 시 해당 항목만 오류 처리하고 나머지는 계속 진행한다

## 8. 테스트/검증

- [ ] 8.1 차트 관련 질문 시 AI 응답에 `[SUGGESTION:...]` 태그가 포함되는지 수동 검증한다
- [ ] 8.2 Action Chip 클릭 → 단일 차트 생성 → 바스켓 저장 흐름을 검증한다
- [ ] 8.3 "다 그려줘" 입력 → 순차 일괄 생성 → 429 에러 미발생을 검증한다
- [ ] 8.4 일반 대화(차트 무관) 시 추천 태그/Action Chip이 나타나지 않는지 검증한다
