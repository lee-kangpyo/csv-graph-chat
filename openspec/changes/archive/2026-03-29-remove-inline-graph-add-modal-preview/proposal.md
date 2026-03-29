## Why

현재 레이아웃은 생성된 그래프를 채팅 영역과 입력창 사이에 인라인으로 보여 주어 세로로 약 400~600px를 쓰고, 대화 읽기가 불편하다. 새 그래프가 나오면 이전 그래프를 다시 볼 수 있는 경로도 없다. 인라인 그래프를 없애 채팅 영역을 넓히고, 바구니에 자동 저장·모달로 보기·썸네일 미리보기로 그래프에 지속적으로 접근할 수 있게 한다.

## What Changes

- **인라인 GraphView 제거**: `App.jsx`에서 `ChatArea`와 `ChatInput` 사이의 그래프 영역 제거
- **생성 그래프 자동 저장**: 채팅으로 그래프가 생성되면 API로 바구니에 자동 저장
- **바구니 항목 클릭 시 모달**: 화면의 약 80% 크기로 그래프 표시, 사용자 질문 함께 표시
- **BasketItem 썸네일/미리보기**: 사이드바 항목에 작은 그래프 미리보기
- **그래프 생성 토스트 제거**: 바구니에서 그래프를 확인할 수 있으므로 생성 알림 토스트는 제거

## Capabilities

### New Capabilities
- `graph-modal-viewing`: 저장된 그래프를 화면 약 80% 크기 모달에 표시하고, 연관된 사용자 질문을 함께 표시
- `graph-basket-preview`: 바구니 사이드바 항목에 그래프 썸네일/미니 미리보기 표시
- `auto-basket-save`: 사용자 수동 조작 없이 생성된 그래프를 바구니에 자동 저장

### Modified Capabilities
- 없음

## Impact

- **프론트엔드**: `App.jsx`(인라인 GraphView 제거), `ChatInput.jsx`(바구니 저장), `BasketItem.jsx`(미리보기·클릭), 신규 `GraphModal` 컴포넌트
- **상태**: `App.jsx`의 `currentGraph` 제거, `basketStore` 중심으로 정리
- **API**: `POST /api/basket/` 호출 증가
- **UX**: 채팅 가독성 향상, 생성된 그래프 지속 접근, UI 단순화
