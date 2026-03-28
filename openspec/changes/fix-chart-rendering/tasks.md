## 1. 백엔드 API 응답 포맷 수정

- [ ] 1.1 `backend/app/api/chat.py`의 `/api/chat/` POST 엔드포인트 응답에 `graph` 필드 추가
- [ ] 1.2 `backend/app/api/chat.py`의 `/api/chat/stream` SSE 스트림 응답에 `graph` 필드 추가

## 2. 프론트엔드 ChatInput 수정

- [ ] 2.1 `frontend/src/components/ChatInput.jsx`에서 API 응답의 `graph` 필드 추출
- [ ] 2.2 `onGraphGenerated(graph)` 콜백 호출 로직 추가

## 3. 프론트엔드 ChatArea SSE 처리

- [ ] 3.1 `frontend/src/components/ChatArea.jsx`에서 SSE 스트림 graph 이벤트 처리
- [ ] 3.2 `frontend/src/api/sseClient.js`에서 `data.graph` 추출하여 콜백 전달

## 4. 검증

- [ ] 4.1 차트 설정이 유효한 object인지 검증 로직 추가
- [ ] 4.2 graph가 null이거나 유효하지 않을 때 렌더링 안 함
