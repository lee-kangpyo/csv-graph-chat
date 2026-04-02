## ADDED Requirements

### Requirement: Data Profile 생성
시스템은 CSV 파일에 대해 Pandas로 실제 통계를 계산하고, file_id 기반 메모리 캐시에 저장해야 한다.

#### Scenario: 신규 파일의 Data Profile 생성
- **WHEN** 채팅 요청이 들어오고 해당 file_id의 프로파일이 캐시에 없으면
- **THEN** 시스템은 CSV를 로드하여 Data Profile을 계산해야 한다
- **AND** 계산된 프로파일을 file_id 키로 메모리 캐시에 저장해야 한다

#### Scenario: 수치형 컬럼 통계 계산
- **WHEN** Data Profile을 계산할 때 수치형 컬럼이 존재하면
- **THEN** 시스템은 각 수치형 컬럼에 대해 평균, 중앙값, 표준편차, 최솟값, 최댓값, null 비율, IQR 기반 이상치 개수를 계산해야 한다

#### Scenario: 카테고리형 컬럼 통계 계산
- **WHEN** Data Profile을 계산할 때 카테고리형 컬럼이 존재하면
- **THEN** 시스템은 각 카테고리형 컬럼에 대해 유니크 값 수와 상위 3개 값 및 해당 비율을 계산해야 한다

#### Scenario: 날짜형 컬럼 통계 계산
- **WHEN** Data Profile을 계산할 때 날짜형 컬럼이 존재하면
- **THEN** 시스템은 시작일, 종료일, 전체 기간(일수)을 계산해야 한다

#### Scenario: 수치형 컬럼 간 상관관계 계산
- **WHEN** 수치형 컬럼이 2개 이상 존재하면
- **THEN** 시스템은 Pearson 상관계수를 계산하여 절댓값 0.5 이상인 컬럼 쌍만 결과에 포함해야 한다

#### Scenario: 대용량 파일 샘플링
- **WHEN** CSV 파일의 행 수가 50,000개를 초과하면
- **THEN** 시스템은 상위 50,000행을 샘플로 통계를 계산하고, 프로파일에 샘플링 여부를 표시해야 한다

#### Scenario: 캐시 재사용
- **WHEN** 동일한 file_id로 채팅 요청이 다시 들어오면
- **THEN** 시스템은 CSV를 재로딩하지 않고 캐시된 Data Profile을 반환해야 한다

#### Scenario: 캐시 용량 초과 시 LRU 제거
- **WHEN** 캐시에 저장된 프로파일 수가 50개를 초과하면
- **THEN** 시스템은 가장 오래 전에 접근된 항목을 제거하고 새 항목을 저장해야 한다
