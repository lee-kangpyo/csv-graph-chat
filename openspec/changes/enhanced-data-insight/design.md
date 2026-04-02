## Context

현재 `/api/chat/stream` 엔드포인트의 AI 인사이트 응답은 `insight_recommendation.py`의 `generate_insight_prompt()`가 생성한다. 이 함수는 `csv_metadata`(컬럼명, 데이터 타입, 3개 샘플 값)만 받아 프롬프트를 구성한다. 결과적으로 LLM은 실제 데이터 분포나 이상치를 확인하지 못한 채 추측성 인사이트를 생성한다.

또한 매 채팅 요청에서 차트 생성 시 `generate_chart_from_file()`이 CSV를 매번 디스크에서 읽는다. 채팅 인사이트 요청도 CSV를 읽도록 변경하면 요청마다 중복 I/O가 발생할 수 있다.

## Goals / Non-Goals

**Goals:**
- Pandas로 실제 통계(이상치, 상관관계, 분포)를 사전 계산하여 LLM 프롬프트에 주입
- 통계를 file_id 기반 메모리 캐시에 저장해 중복 계산 방지
- System 프롬프트를 3단계 구조(Persona → 실제 통계 → 분석 프레임워크)로 재설계
- 컬럼 수에 따른 토큰 예산 자동 조절로 응답 지연 방지

**Non-Goals:**
- 대화 히스토리(멀티턴) 구현 — 별도 변경으로 다룬다
- 프론트엔드 변경 — API 시그니처 유지로 불필요
- 외부 캐시 스토어(Redis 등) 도입 — process-level 메모리 캐시로 충분

## Decisions

### Decision 1: 캐시 위치 — 모듈 레벨 dict

**선택**: `pandas_processor.py`에 `_profile_cache: dict[str, DataProfile]` 모듈 레벨 변수로 캐싱

**대안 고려**:
- *파일 시스템 캐시(JSON 저장)*: 서버 재시작 후에도 유지되지만, 파일 I/O와 직렬화 복잡성 증가
- *업로드 API 응답에 통계 포함*: 프론트엔드 변경 필요, API 계약 변경

**이유**: 서버 재시작 시 캐시 소멸은 허용 가능 (재업로드 시 재계산). 구현 복잡도 최소화.

---

### Decision 2: 통계 계산 시점 — 첫 번째 채팅 요청 시 lazy compute

**선택**: 채팅 요청이 들어올 때 캐시 miss이면 그 시점에 CSV를 읽어 계산 (lazy)

**대안 고려**:
- *업로드 시점에 즉시 계산*: `upload.py` 수정 필요, 업로드 응답 지연 발생 가능
- *백그라운드 태스크*: FastAPI BackgroundTask 추가로 복잡도 증가

**이유**: 업로드 후 채팅을 안 할 수도 있다. Lazy compute가 실제 필요 시에만 비용 지불.

---

### Decision 3: 토큰 예산 — 컬럼 수 임계값 기반 축약

**선택**:
- 컬럼 ≤ 10개: 전체 통계 주입
- 컬럼 > 10개: 핵심 이상치/상관관계 상위 5개만 주입 + 요약 한 줄

**이유**: 평균 LLM context window에서 system prompt가 4000 토큰 초과 시 응답 품질 저하 및 비용 급증.

---

### Decision 4: 질문 관련 컬럼 선별 주입

**선택**: 사용자 질문에서 컬럼명을 문자열 매칭으로 감지, 해당 컬럼의 통계를 우선 배치

**대안 고려**:
- *LLM이 관련 컬럼 판단*: 추가 LLM 호출 필요, 비용/지연 증가
- *전체 통계 항상 주입*: 토큰 폭발 위험

**이유**: 단순 문자열 매칭으로도 80% 케이스 커버 가능. 추가 비용 0.

## Risks / Trade-offs

- **[Risk] 첫 채팅 응답 지연**: Lazy compute로 첫 요청에 CSV 로딩 + 통계 계산 추가됨  
  → **Mitigation**: 계산 시간 로깅으로 모니터링, 50MB 이상 파일은 샘플링(head 5000행)으로 처리

- **[Risk] 메모리 누수**: process가 장시간 실행되면 캐시가 무한 증가  
  → **Mitigation**: 캐시 최대 50개 제한, LRU 방식으로 오래된 항목 제거

- **[Risk] 컬럼명 매칭 오탐**: "sales"를 질문에서 못 찾으면 관련 통계 미주입  
  → **Mitigation**: 매칭 실패 시 전체 통계의 요약 버전(핵심 이상치/상관관계)은 항상 포함

- **[Trade-off] 통계 기반 인사이트 vs. LLM 창의성**: 실제 수치를 제공하면 LLM이 사실에 구속됨  
  → 이는 목표이므로 trade-off 허용. 추측보다 정확한 인사이트가 더 가치 있음.

## Migration Plan

1. `pandas_processor.py`에 `compute_data_statistics()` 및 캐시 로직 추가
2. `insight_recommendation.py`의 `generate_insight_prompt()` 파라미터 및 템플릿 확장
3. `chat.py`의 `generate_chat_response()`에서 캐시 조회 → 통계 주입 흐름 연결
4. 기존 API 시그니처 유지 — 롤백 시 `generate_chat_response()` 내 통계 조회 라인만 제거

**롤백**: `chat.py`에서 `data_statistics=None`으로 호출하면 기존 동작과 동일.
