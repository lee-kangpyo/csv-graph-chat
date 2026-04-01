## MODIFIED Requirements

### Requirement: 모달 오버레이로 그래프 표시
#### Scenario: BasketItem 클릭으로 그래프 보기
- **WHEN** 사용자가 사이드바에서 BasketItem을 클릭할 때
- **AND** 해당 항목에 유효한 `graph_config`가 존재할 때
- **THEN** 화면 중앙에 모달 오버레이가 표시된다
- **AND** 모달 크기는 화면 너비·높이의 약 80%이다
- **AND** 모달 안에 그래프가 충분한 크기로 렌더링된다
- **AND** 해당 그래프를 만든 사용자 질문이 함께 표시된다
- **AND** 배경은 어둡게 처리된다
- **AND** 나머지 화면은 오버레이로 가려진다

#### Scenario: 로딩 placeholder 클릭 시 모달 금지
- **WHEN** BasketItem이 로딩 placeholder 상태(`graph_config` 없음)일 때
- **THEN** 클릭해도 모달 오버레이는 열려서는 안 된다
