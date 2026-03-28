## Context

CSV 파일을 업로드하고 AI와 대화형으로 데이터를 분석하여 그래프를 생성한 후, 바구니에 저장하고 다운로드하는 MVP를 구축합니다.

**현재 상태**: 없음 (신규 프로젝트)

**제약사항**:
- 세션 관리 없음 (페이지 리로드 시 상태 초기화)
- 단일 CSV 파일만 처리 (나중에 여러 개 추가 가능)
- 10MB 이하 파일만 허용
- 토스트 메시지로 에러/성공 표시 (3초 후 자동 사라짐)

**관계자**: End-user (데이터 분석이 필요한 사용자)

## Goals / Non-Goals

**Goals:**
- CSV 업로드 시 헤더 자동 감지 및 AI 컬럼명 추론
- AI가 데이터 구조를 파악 후 "어떤 인사이트를 원하세요?"로 질문
- SSE 기반 실시간 AI 대화 (타이핑 효과)
- 자연어로 그래프 수정 요청 ("지역별로 나눠줘", "색깔 바꿔줘")
- 바구니에 그래프 저장, 목록, 미리보기, 삭제
- 바구니 전체 HTML 다운로드

**Non-Goals:**
- 다중 CSV 파일 처리 (Phase 2)
- 로그인/회원가입 (Phase 2)
- CSV 재사용 (이전 파일 목록) (Phase 2)
- 고급 분석 (clustering, anomaly detection) (Phase 2)
- 사용자당 데이터 격리 (단일 사용자 MVP)

## Decisions

### 1. Backend: FastAPI + DuckDB

**결정**: PostgreSQL 대신 DuckDB 사용

**이유**:
- In-Process DB로 별도 서버 설치 불필요
- CSV 파일을 직접 테이블처럼 쿼리 가능
- OLAP 분석에 최적화된 속도
- MVP 개발 속도 향상
- 나중에 PostgreSQL로 마이그레이션 가능

**대안**: PostgreSQL (설치/설정 복잡, CSV 저장 방식 별도 설계 필요)

### 2. Frontend: React + Vite + Zustand + TailwindCSS

**결정**: React SPA 구조

**이유**:
- Vite: 빠른 개발 서버 및 빌드
- Zustand: 간결한 상태 관리 (Context API보다 명확한 분리)
- TailwindCSS: 빠른 UI 개발 (CSS 작성 불필요)

**대안**: Vue.js (유사한 장점, React 선택)

### 3. 통신: Axios (upload/CRUD) + SSE (AI streaming)

**결정**: 하이브리드 접근

**이유**:
- Axios: CSV 업로드, 바구니 CRUD (request/response에 적합)
- SSE: AI 대화 스트리밍 (실시간 텍스트 + 그래프 설정 수신)

**대안**:
- WebSocket (과도한 복잡성, MVP엔 불필요)
- Long Polling (SSE보다 구현 복잡)

### 4. 차트 라이브러리: Chart.js

**결정**: CDN에서 로드

**이유**:
-轻量级 (4种 기본 차트 타입 지원)
- 설정이 단순 (JS 객체로 차트 설정 전달)
- HTML 다운로드 시 차트 설정 그대로 포함 가능

### 5. LLM: z.ai 코딩 플랜

**결정**: OpenAI API와 호환되는 z.ai 사용

**이유**:
- 비용 효율적 (OpenAI 대비)
- 나중에 OpenAI 등 다른 provider로 교체 용이

## Risks / Trade-offs

| Risk | Mitigation |
|------|------------|
| DuckDB In-Process 특성상 다중 사용자 환경 한계 | Phase 2에서 PostgreSQL 마이그레이션 |
| SSE 연결 단절 시 재연결 필요 | EventSource 자동 재연결 활용 |
| 큰 CSV 파일 (100MB+) 처리 문제 | 10MB 제한으로 예방, 필요시 샘플링 추가 |
| LLM 응답 지연 (5-10초) | SSE streaming으로 실시간 피드백 제공 |

## Migration Plan

**Phase 1 (MVP)**:
1. 로컬에서 FastAPI + React 개발
2. DuckDB로 CSV 분석
3. 단일 사용자 테스트

**Phase 2 (확장)**:
1. PostgreSQL 전환 (필요시)
2. 다중 CSV 지원
3. 사용자 인증 추가

**Rollback**: 해당 없음 (MVP라서)

## Open Questions

1. **바구니 HTML 다운로드**: 각 그래프별 개별 HTML? 하나의 ZIP?
2. **CSV 데이터 저장 기간**: 세션 종료 후 CSV 재사용 불가?
3. **LLM provider 교체 시**: abstraction layer 필요 여부
