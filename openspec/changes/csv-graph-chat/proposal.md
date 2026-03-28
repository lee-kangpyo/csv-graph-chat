## Why

사용자가 CSV 파일을 업로드하면 AI와 대화형으로 데이터를 분석하고, 원하는 그래프를 자동으로 생성한 후 나중에 모아서 다운로드하는 도구가 필요합니다. 기존 방식은 CSV → Excel/Google Sheets → 그래프 생성 → 저장이라는 수동 절차를 거치는데, AI를 활용하면 사용자가 "어떤 데이터 분석을 원하세요?"라고 묻고 직접 그래프를 만들어낼 수 있습니다.

## What Changes

- **CSV 업로드 + AI 분석**: 파일 업로드 시 헤더 자동 감지 및 AI가 컬럼 의미 추론. 사용자가 대화로 컬럼명 수정 가능.
- **대화형 그래프 생성**: AI가 데이터 구조를 파악한 후 "어떤 인사이트를 원하세요?"라고 질문. 사용자가 요청하면 그래프 생성.
- **실시간 그래프 수정**: "지역별로 나눠줘", "색깔 바꿔줘" 등 자연어로 수정 요청 가능.
- **바구니 저장 기능**: 생성된 그래프를 바구니에 저장. 목록 확인, 미리보기, 개별 삭제 가능.
- **일괄 다운로드**: 바구니의 그래프들을 HTML 파일로 다운로드.
- **에러 처리**: 토스트 메시지로 파일 크기 초과, API 실패 등 사용자에게 안내 (3초 후 자동 사라짐).
- **파일 크기 제한**: 10MB 이하의 CSV만 허용.

## Capabilities

### New Capabilities

- `csv-upload-analysis`: CSV 파일 업로드, 헤더 자동 감지, 데이터 타입 탐지, AI 컬럼명 추론, 사용자 수정 기능
- `ai-graph-conversation`: AI와 SSE 기반 실시간 대화, 인사이트 추천, SQL 생성 (DuckDB용), 그래프 설정 생성
- `graph-basket`: 그래프 설정 저장, 목록 조회, 미리보기, 개별 삭제, 일괄 HTML 다운로드
- `chart-rendering`: Chart.js 기반 꺾은선/막대/도넛/산점도 그래프 렌더링, 실시간 업데이트

### Modified Capabilities

없음 (신규 프로젝트)

## Impact

- **신규 프로젝트**: `csv-graph-chat/` (FastAPI 백엔드 + React 프론트엔드)
- **백엔드 의존성**: FastAPI, duckdb, openai (또는 z.ai), python-multipart, sse-starlette
- **프론트엔드 의존성**: React, Vite, Zustand, TailwindCSS, Chart.js, Axios
- **데이터 저장**: DuckDB (In-Process, CSV 파일 직접 읽기)
- **세션**: 세션 관리 없음 (페이지 리로드 시 상태 초기화)
