## 1. Data Profile 계산 함수 구현 (pandas_processor.py)

- [ ] 1.1 `compute_data_statistics(df, columns)` 함수 skeleton 작성 — 반환 타입 `dict` 정의
- [ ] 1.2 수치형 컬럼 처리: 평균, 중앙값, 표준편차, min/max, null 비율, IQR 기반 이상치 개수 계산
- [ ] 1.3 카테고리형 컬럼 처리: 유니크 값 수, 상위 3개 값 + 비율 계산
- [ ] 1.4 날짜형 컬럼 처리: 시작일, 종료일, 기간(일수) 계산
- [ ] 1.5 Pearson 상관계수 계산 — 절댓값 0.5 이상 쌍만 결과에 포함
- [ ] 1.6 50,000행 초과 시 샘플링 로직 추가 및 `sampled: true` 플래그 포함

## 2. 메모리 캐시 구현 (pandas_processor.py)

- [ ] 2.1 모듈 레벨 `_profile_cache: OrderedDict` 변수 선언 (LRU를 위해 OrderedDict 사용)
- [ ] 2.2 `get_or_compute_profile(file_path, file_id, columns)` 함수 구현 — 캐시 hit/miss 처리
- [ ] 2.3 캐시 항목 50개 초과 시 LRU(가장 오래된 항목) 제거 로직 구현

## 3. 프롬프트 재설계 (insight_recommendation.py)

- [ ] 3.1 `generate_insight_prompt()` 파라미터에 `data_statistics: Optional[dict] = None` 추가
- [ ] 3.2 Section 1 — Analyst Persona 텍스트 작성: 사실 기반 분석, 추측 금지 지침 포함
- [ ] 3.3 Section 2 — Data Profile 포맷터 함수 `_format_statistics_for_prompt(data_statistics, columns, user_question)` 작성
- [ ] 3.4 컬럼 수 ≤ 10: 전체 통계 주입 / > 10: 이상치 top 5 + 상관관계 top 5 + 질문 관련 컬럼만 주입 분기 처리
- [ ] 3.5 질문에서 컬럼명 감지 로직 구현 — 단순 문자열 포함 여부 검사
- [ ] 3.6 Section 3 — 분석 프레임워크 텍스트 작성: 이상치 → 추세 → 상관관계 → 세그먼트 → 액션 순서 지침

## 4. chat.py 연결

- [ ] 4.1 `generate_chat_response()`에서 `file_id`가 있을 때 `get_or_compute_profile()` 호출 로직 추가
- [ ] 4.2 CSV 파일 경로 구성 로직 추가 (기존 `generate_chart_from_file()`의 경로 구성 방식 참고)
- [ ] 4.3 `generate_insight_prompt()` 호출 시 `data_statistics` 인수 전달

## 5. 검증

- [ ] 5.1 백엔드 서버 재시작 후 import 에러 없음 확인
- [ ] 5.2 수치형 + 카테고리형 + 날짜형 컬럼이 모두 포함된 CSV로 채팅 요청 — 응답에 실제 수치 포함 확인
- [ ] 5.3 동일 파일로 두 번 채팅 요청 — 두 번째 요청 로그에 캐시 hit 확인
- [ ] 5.4 컬럼 10개 초과 CSV로 요청 — 프롬프트 토큰 축약 동작 확인 (서버 로그)
- [ ] 5.5 "이 데이터에서 이상한 점이 있어?" 질문 시 구체적인 이상치 개수/컬럼명 응답 확인
