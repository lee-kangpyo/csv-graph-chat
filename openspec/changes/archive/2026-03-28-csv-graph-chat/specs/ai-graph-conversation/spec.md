## ADDED Requirements

### Requirement: AI 인사이트 추천
CSV 데이터를 분석한 후, 시스템은 AI가 사용자에게 원하는 인사이트를 물어봐야 한다.

#### Scenario: 데이터 타입 기반 AI 추천
- **WHEN** CSV에 Date + Number 컬럼이 있으면
- **THEN** AI는 "시계열 추이"를 추천해야 한다
- **AND** 월별/분기별/연간 비교 옵션을 제시해야 한다

#### Scenario: 그룹 비교 추천
- **WHEN** CSV에 Category + Number 컬럼이 있으면
- **THEN** AI는 "그룹별 비교"를 추천해야 한다
- **AND** 막대 그래프나 파이 차트를 제안해야 한다

#### Scenario: 직접 요청 옵션 제공
- **WHEN** AI가 추천 인사이트를 제시하면
- **THEN** "직접 설명해주세요" 옵션도 함께 제시해야 한다
- **AND** 사용자의 직접적인 요청을 기다려야 한다

### Requirement: 자연어로 그래프 수정
시스템은 사용자가 자연어 명령으로 그래프를 수정할 수 있어야 한다.

#### Scenario: 차트 타입 변경
- **WHEN** 사용자가 "지역별로 나눠줘" 또는 "막대 그래프로 바꿔줘"라고 하면
- **THEN** 시스템은 그에 따라 그래프를 업데이트해야 한다
- **AND** 변경 사항을 확인해야 한다

#### Scenario: 색상/스타일 변경
- **WHEN** 사용자가 "색깔 바꿔줘" 또는 "파란색으로 해줘"라고 하면
- **THEN** 시스템은 차트 색상을 업데이트해야 한다
- **AND** 수정된 그래프를 보여줘야 한다

#### Scenario: 데이터 범위 필터링
- **WHEN** 사용자가 "1월만 보여줘" 또는 "이상치 제외해줘"라고 하면
- **THEN** 시스템은 필터링된 데이터로 그래프를 업데이트해야 한다
- **AND** 적용된 필터를 확인해야 한다

#### Scenario: 추세선 추가
- **WHEN** 사용자가 "trend line 추가해줘"라고 하면
- **THEN** 시스템은 기존 차트에 추세선을 추가해야 한다

### Requirement: 실시간 스트리밍 응답
시스템은 Server-Sent Events(SSE)를 사용하여 AI 응답을 실시간으로 전달해야 한다.

#### Scenario: AI 타이핑 효과
- **WHEN** AI가 요청을 처리 중일 때
- **THEN** 시스템은 응답 텍스트를 캐릭터 단위로 스트리밍해야 한다
- **AND** 도착하는 대로 채팅 영역에 표시해야 한다

#### Scenario: 그래프 생성 알림
- **WHEN** AI가 그래프 생성을 결정하면
- **THEN** 시스템은 "그래프 생성 중..." 같은 중간 메시지를 보내야 한다
- **AND** 최종 그래프 설정을 스트리밍해야 한다

#### Scenario: SSE 타임아웃 처리
- **WHEN** SSE 연결이 30초 타임아웃될 때
- **THEN** 시스템은 토스트 에러 "AI 응답 시간이 초과되었습니다. 다시 시도해주세요"를 표시해야 한다
- **AND** 사용자가 재시도할 수 있도록 해야 한다

### Requirement: DuckDB용 SQL 생성
시스템은 CSV 데이터를 분석하기 위해 DuckDB가 실행할 수 있는 SQL 쿼리를 생성해야 한다.

#### Scenario: GROUP BY 쿼리 생성
- **WHEN** 사용자가 "지역별 매출"이라고 요청하면
- **THEN** AI는 SQL을 생성해야 한다: `SELECT region, SUM(sales) FROM 'data.csv' GROUP BY region`

#### Scenario: 시계열 쿼리 생성
- **WHEN** 사용자가 "월별 추이"라고 요청하면
- **THEN** AI는 감지된 날짜 컬럼 기반의 날짜 그룹화 SQL을 생성해야 한다

#### Scenario: 복잡한 집계를 위한 쿼리 생성
- **WHEN** 사용자가 "지역별 월별 매출 히트맵"이라고 요청하면
- **THEN** AI는 적절한 피벗 스타일 SQL 쿼리를 생성해야 한다

### Requirement: 그래프 설정 출력
시스템은 ECharts가 렌더링할 수 있는 형식으로 그래프 설정을 출력해야 한다.

#### Scenario: 꺾은선 그래프 설정
- **WHEN** AI가 꺾은선 그래프를 생성하면
- **THEN** 출력은 series.type = "line"인 ECharts 형식을 포함해야 한다

#### Scenario: 막대 그래프 설정
- **WHEN** AI가 막대 그래프를 생성하면
- **THEN** 출력은 series.type = "bar"인 ECharts 형식을 포함해야 한다

#### Scenario: 파이 차트 설정
- **WHEN** AI가 파이 차트를 생성하면
- **THEN** 출력은 series.type = "pie"인 ECharts 형식을 포함해야 한다

#### Scenario: 산점도 설정
- **WHEN** AI가 산점도를 생성하면
- **THEN** 출력은 series.type = "scatter"인 ECharts 형식을 포함해야 한다

#### Scenario: 히트맵 설정
- **WHEN** AI가 히트맵을 생성하면
- **THEN** 출력은 series.type = "heatmap"인 ECharts 형식을 포함해야 한다
- **AND** 날짜 기반 히트맵(월별, 분기별)을 지원해야 한다

#### Scenario: 고급 차트 타입 (산키, 선버스트)
- **WHEN** AI가 데이터가 산키 또는 선버스트에 적합하다고 판단하면
- **THEN** 출력은 적절한 ECharts 타입을 포함해야 한다
