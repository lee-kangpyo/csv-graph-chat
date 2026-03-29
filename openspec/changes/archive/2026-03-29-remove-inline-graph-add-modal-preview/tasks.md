## 1. GraphModal 컴포넌트

- [x] 1.1 `GraphModal.jsx` 생성 — 오버레이·모달 컨테이너 구조
- [x] 1.2 모달 크기 스타일(화면 너비·높이 약 80%)
- [x] 1.3 헤더 닫기 버튼(X)
- [x] 1.4 오버레이 클릭 시 닫기
- [x] 1.5 props: graph config, 사용자 질문, `onClose`
- [x] 1.6 모달 내부 ECharts 인스턴스 및 리사이즈 처리
- [x] 1.7 헤더에 사용자 질문 표시(최소 14px, 줄바꿈)
- [x] 1.8 z-index 1000
- [ ] 1.9 line, bar, pie 등 여러 차트 타입으로 모달 렌더링 수동 테스트

## 2. BasketItem 컴포넌트

- [x] 2.1 클릭 시 `GraphModal` 열기
- [x] 2.2 미니 ECharts 컨테이너(150×100px)
- [x] 2.3 축소된 config로 미리보기 렌더링
- [x] 2.4 이름 옆 또는 위에 미리보기 배치
- [x] 2.5 미리보기 로딩 상태
- [ ] 2.6 미리보기 클릭 시 모달 열림 확인
- [ ] 2.7 바구니 20개 이상일 때 미리보기 성능 확인

## 3. ChatInput — 자동 바구니 저장

- [x] 3.1 `basketApi`의 `createBasket` 등 import
- [x] 3.2 그래프 생성 시 채팅 맥락에서 사용자 질문 추출
- [x] 3.3 그래프 이름 생성(50자 자르기, 특수문자 처리)
- [x] 3.4 일반적 질문용 폴백 이름(`Graph [timestamp]` 등)
- [x] 3.5 그래프 생성 시 `POST /api/basket/` 호출(name, graph_config, question)
- [x] 3.6 저장 실패 시 UI 피드백
- [x] 3.7 생성 직후 `basketStore` 낙관적 업데이트
- [x] 3.8 API 실패 시 롤백
- [x] 3.9 저장이 채팅 동작을 막지 않도록 처리

## 4. App 컴포넌트

- [x] 4.1 `currentGraph` 상태 제거
- [x] 4.2 `ChatArea`에서 `onGraphGenerated` 제거
- [x] 4.3 `ChatInput`에서 `onGraphGenerated` 제거
- [x] 4.4 `ChatArea`와 `ChatInput` 사이 인라인 `GraphView` 제거
- [x] 4.5 모달 상태(`selectedGraph`, `isOpen` 등)
- [x] 4.6 모달 열기/닫기 및 선택 그래프 데이터 전달
- [x] 4.7 `isOpen`일 때 `GraphModal` 렌더
- [x] 4.8 열릴 때 graph 데이터·질문 전달
- [x] 4.9 `BasketSidebar`/`BasketItem`에 모달 열기 핸들러 전달

## 5. BasketSidebar

- [x] 5.1 `onGraphClick`(또는 동등) prop으로 항목 클릭 전달
- [x] 5.2 `BasketItem`에 핸들러 전달
- [x] 5.3 채팅 생성 그래프가 바구니 목록에 반영되는지 확인
- [ ] 5.4 그래프 생성 후 바구니 갱신 수동 테스트

## 6. 상태 정리

- [x] 6.1 `ChatInput` 등에서 `setCurrentGraph` 사용 제거
- [x] 6.2 `basketStore` 낙관적 업데이트 연동 확인
- [ ] 6.3 채팅 생성 → 저장 흐름 수동 테스트
- [ ] 6.4 미리보기 ECharts 인스턴스 메모리 누수 없는지 확인

## 7. 테스트·검증

- [ ] 7.1 그래프 생성 및 자동 바구니 저장 플로우
- [ ] 7.2 차트 타입별 `BasketItem` 미리보기
- [ ] 7.3 `GraphModal` 열기/닫기
- [ ] 7.4 모달에 사용자 질문 표시
- [ ] 7.5 바구니 저장 실패 처리
- [ ] 7.6 낙관적 업데이트·롤백
- [ ] 7.7 연속으로 여러 그래프 생성
- [ ] 7.8 바구니 20개 이상 성능
- [ ] 7.9 모달 z-index와 기존 토스트
- [ ] 7.10 모달 반응형(화면 크기)
- [ ] 7.11 다양한 질문으로 그래프 이름 생성
- [ ] 7.12 모달 바깥(오버레이) 클릭 닫기
- [ ] 7.13 모달 열린 상태에서 바구니 사이드바 접근성
