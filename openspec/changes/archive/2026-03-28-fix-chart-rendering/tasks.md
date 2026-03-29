## 1. 백엔드 API 응답 포맷 수정

- [x] 1.1 `backend/app/api/chat.py`의 `/api/chat/` POST 엔드포인트 응답에 `graph` 필드 추가
- [x] 1.2 `backend/app/api/chat.py`의 `/api/chat/stream` SSE 스트림 응답에 `graph` 필드 추가

## 2. 프론트엔드 ChatInput 수정

- [x] 2.1 `frontend/src/components/ChatInput.jsx`에서 API 응답의 `graph` 필드 추출
- [x] 2.2 `onGraphGenerated(graph)` 콜백 호출 로직 추가

## 3. 프론트엔드 ChatArea SSE 처리

- [x] 3.1 `frontend/src/components/ChatArea.jsx`에서 SSE 스트림 graph 이벤트 처리
- [x] 3.2 `frontend/src/api/sseClient.js`에서 `data.graph` 추출하여 콜백 전달

## 4. 검증

- [x] 4.1 차트 설정이 유효한 object인지 검증 로직 추가
- [x] 4.2 graph가 null이거나 유효하지 않을 때 렌더링 안 함

## 5. 차트 생성 로직

- [x] 5.1 `detect_chart_request()` - 사용자 메시지에서 차트 요청 감지
- [x] 5.2 `detect_chart_type()` - 차트 타입 결정 (line, bar, pie 등)
- [x] 5.3 `generate_chart_from_csv_metadata()` - CSV 메타데이터 기반 차트 설정 생성
- [x] 5.4 data_type="unknown"인 경우 sample_values로 타입 추론
- [x] 5.5 차트 요청 시 graph 설정 반환, 미요청 시 graph: null

## 6. 테스트

- [x] 6.1 실제 데이터 포맷 (data_type: unknown) 테스트
- [x] 6.2 빈 columns, None metadata 엣지 케이스 테스트
- [x] 6.3 SSE done event에 graph 포함 테스트
