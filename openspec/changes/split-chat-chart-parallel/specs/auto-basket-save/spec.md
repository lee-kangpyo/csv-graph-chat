## MODIFIED Requirements

### Requirement: 낙관적 바구니 갱신
#### Scenario: 생성 직후 바구니에 즉시 반영
- **WHEN** 채팅에서 그래프 생성이 시작될 때(차트 요청으로 판단될 때)
- **THEN** 바구니 사이드바에 **로딩 placeholder 항목**이 즉시 나타나야 한다
- **AND** placeholder 항목은 `graph_config`가 준비되기 전까지 로딩 상태로 표시되어야 한다
- **AND** `POST /api/chart/generate`가 성공하여 `graph`가 준비되면 placeholder를 제거하고 기존과 동일하게 `POST /api/basket/`로 최종 저장되어야 한다
- **AND** 생성 실패 시 placeholder는 제거되고 오류가 표시되어야 한다

### Requirement: 생성 그래프 자동 바구니 저장
#### Scenario: 채팅에서 그래프 생성 시 저장
- **WHEN** AI가 사용자 질문에 따라 그래프를 생성할 때
- **THEN** 최종적으로는 즉시 `POST /api/basket/`로 그래프 설정을 전송해야 한다
- **AND** 최종 저장 전 단계에서 placeholder 로딩 항목이 사용자에게 진행 상태를 제공해야 한다
