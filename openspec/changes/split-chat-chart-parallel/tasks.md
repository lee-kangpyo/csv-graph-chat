## 1. 백엔드: 채팅 SSE를 텍스트 전용으로 분리

- [ ] 1.1 `backend/app/api/chat.py`의 `/api/chat/stream`에서 `generate_chart_from_file()` 호출을 제거한다
- [ ] 1.2 SSE `message`/`done` payload에 `request_id`를 포함할 수 있게 한다(프론트 상관 처리)

## 2. 백엔드: 그래프 생성 전용 API 추가

- [ ] 2.1 `POST /api/chart/generate` 라우터를 추가한다
- [ ] 2.2 요청 바디: `message`, `csv_metadata`, `request_id`
- [ ] 2.3 응답 바디: `request_id`, `graph`(object|null)
- [ ] 2.4 내부 구현은 기존 `generate_chart_from_file()` 로직을 재사용한다
- [ ] 2.5 `backend/app/main.py`에 라우터를 등록한다

## 3. 프론트: 차트 요청 시 병렬 호출 + 바스켓 placeholder

- [ ] 3.1 `frontend/src/components/ChatInput.jsx`에서 차트 요청이면:
  - 바스켓에 placeholder 항목을 즉시 추가한다(`graph_config: null`, 로딩 표시)
  - `/api/chat/stream` SSE 시작
  - 동시에 `/api/chart/generate` 호출
- [ ] 3.2 SSE 수신으로 마지막 AI 메시지 텍스트를 스트리밍 업데이트한다
- [ ] 3.3 chart generate 성공 시 placeholder를 제거하고 `createBasket()`로 최종 저장/교체한다
- [ ] 3.4 실패 시 placeholder 제거 + 토스트 오류

## 4. 프론트: placeholder 클릭 제한

- [ ] 4.1 `frontend/src/components/BasketItem.jsx`에서 `graph_config`가 없으면 클릭으로 모달을 열지 않는다
- [ ] 4.2 로딩 UI(스피너/문구)를 명확히 표시한다

## 5. 테스트/검증

- [ ] 5.1 `backend/tests/test_chart_rendering_spec.py` 갱신:
  - SSE message 이벤트에 graph 필드가 **없어야** 하는 계약(또는 항상 null) 검증
  - chart generate 엔드포인트 응답 계약 검증(새 테스트 추가)
