## Why

현재 AI 인사이트 추천 시스템은 LLM에게 컬럼명과 수 개의 샘플 값만 전달하여, LLM이 실제 데이터를 보지 못한 채 추측성 인사이트를 생성한다. "컬럼 A와 B의 상관관계가 높을 것 같습니다"처럼 사실 근거 없는 답변이 나오는 근본 원인이다. 또한 매 채팅 요청마다 CSV를 반복 로딩하는 비효율도 존재한다.

## What Changes

- **Pandas 기반 Data Profile 사전 계산**: CSV 업로드 시점에 수치/카테고리/날짜형 컬럼별 통계(평균, 중앙값, 표준편차, 이상치 수, null 비율, 상관관계 등)를 한 번 계산하고 캐싱
- **프롬프트 구조 재설계**: System 프롬프트를 3단계로 재편 — (1) Analyst Persona, (2) 실제 통계값 주입, (3) 분석 프레임워크(이상치→추세→상관관계→세그먼트→액션 순서)
- **선별적 통계 주입**: 사용자 질문 키워드와 컬럼을 매칭하여 관련 통계만 주입, 토큰 폭발 방지
- **토큰 예산 관리**: 컬럼 수 기준으로 주입 정보량 자동 조절 (10개 이하: 전체, 초과: 핵심 요약)
- **chat.py 수정**: `generate_chat_response()`가 캐시된 Data Profile을 활용하도록 변경

## Capabilities

### New Capabilities
- `data-profiling`: CSV 업로드 시 Pandas로 실제 통계를 계산하고, file_id 기반으로 메모리 캐싱하는 Data Profile 생성/관리 시스템

### Modified Capabilities
- `ai-graph-conversation`: AI 인사이트 추천의 근거가 추측에서 실제 계산된 통계로 변경됨 — LLM 프롬프트에 Data Profile 기반 사실 정보가 주입되는 요구사항 추가

## Impact

- **Backend**: `pandas_processor.py` (통계 계산 함수 추가), `insight_recommendation.py` (프롬프트 재설계), `chat.py` (Data Profile 로딩 및 주입 로직)
- **API 변경 없음**: `/api/chat/stream`, `/api/chat/` 엔드포인트 시그니처 유지
- **Dependencies**: 추가 라이브러리 없음 (pandas, numpy 이미 사용 중)
- **성능**: 업로드 시 통계 계산 1회 추가, 이후 요청은 캐시 활용으로 오히려 개선
