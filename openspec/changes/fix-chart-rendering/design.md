## Context

현재 아키텍처:
- **프론트엔드**: ECharts 기반 차트 렌더링 인프라 (GraphView.jsx, graphStore.js) 존재
- **백엔드**: LLM 기반 대화 API (`/api/chat/`, `/api/chat/stream`) 구현済み
- **문제**: 백엔드가 차트 설정을 생성하지 않음, 프론트엔드가 차트 설정을 처리하지 않음

기존 `chart-rendering` 스펙에는 "AI가 ECharts 설정을 생성하면 렌더링해야 한다"는 요구사항이 있지만, 구현이 미완성인 상태.

## Goals / Non-Goals

**Goals:**
- AI 대화 응답에 ECharts 차트 설정이 포함될 때 프론트엔드에서 렌더링
- 기존 SSE 스트림 응답 처리에서 graph 이벤트 지원
- 차트 설정은 ECharts가 직접 렌더링할 수 있는 완전한 config 객체形式

**Non-Goals:**
- LLM이 직접 완전한 ECharts JSON을 생성하도록 하는 것은 별도 스펙에서 다룸
- 차트 다운로드 (htmlDownload.js) 기능은 이미 존재하므로 수정 없음
- 다양한 차트 타입 최적화는 후속 작업으로 미룸

## Decisions

### 1. API 응답 포맷 변경

**선택**: 기존 `{"content": string}` 응답에 `graph` 필드 추가

```json
{
  "content": "분석 완료...",
  "graph": { "series": [...], "xAxis": {...}, "yAxis": {...} }
}
```

**이유**: 
- 기존 API 계약-breaking 변경 최소화
- graph가 없으면 차트 렌더링 안 함 (기존 동작 유지)

### 2. 프론트엔드 차트 상태 관리

**선택**: `graphStore`의 `currentGraph` 사용 (이미 존재)

**이유**:
- GraphView.jsx가 이미 `currentGraph` prop을 받도록 구현됨
- App.jsx에서 `setCurrentGraph` 상태 업데이트机制 존재

### 3. SSE 스트림 처리

**선택**: SSE 이벤트에 `graph` 필드 추가

```javascript
// 백엔드
yield { "event": "message", "data": JSON.stringify({ content: "...", graph: {...} }) }
```

**이유**:
- 기존 SSE 스트림 구조 유지
- `sseClient.js`의 `onMessage` 콜백이 `data.content`만 사용하므로 `data.graph` 추가

### 4. 차트 설정 생성 위치

**선택**: 백엔드 `chat.py` 또는 새 모듈에서 LLM 응답 기반 생성

**이유**:
- `app/api/graph_config.py`에 이미 `generate_echarts_config_from_llm()` 존재
- 기존 `llm_client.py`와 분리하여 책임 분리

## Risks / Trade-offs

- [Risk] LLM 응답 파싱이 잘못될 경우 잘못된 차트 설정이 렌더링
  - → Mitigation: graph 필드가 유효한 JSON object인지 검증
- [Risk] SSE 스트림에서 graph와 content 타이밍 불일치
  - → Mitigation: graph는 마지막 message 또는 별도 event로送信
- [Trade-off] API 응답에 graph 포함 시 토큰 증가
  - → 현재 구조상 chat.py의 `/` POST만 수정 (SSE는 future work)

## Open Questions

1. SSE 스트림에서 차트 설정 전송时机 (마지막 chunk vs 별도 event)?
2. LLM이 차트 필요性を判断하는 로직 위치 (백엔드 vs 프론트엔드)?
