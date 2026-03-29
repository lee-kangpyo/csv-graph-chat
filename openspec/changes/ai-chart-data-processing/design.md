## Context

현재 아키텍처:
- `chat.py`의 `generate_chart_from_csv_metadata()`가 CSV 파일을 로드하지만, 실제 데이터를 분석하지 않고 더미 데이터를 생성
- 라벨: `["Item 1", "Item 2", ...]`
- 데이터: `[50.0, 100.0, ...]`
- 실제 CSV 컬럼명, 값, 그룹화 정보가 사용되지 않음

문제:
- "학과별 평균 평점" 요청 시 실제 학과별 평점 데이터가 아닌 의미 없는 데이터 표시
- LLM이 CSV 정보를 전혀 활용하지 않음

## Goals / Non-Goals

**Goals:**
- LLM이 CSV 헤더 + 샘플 데이터로 분석 intent 결정
- 분석 intent를 구조화된 형태(JSON)로 파싱
- pandas로 실제 groupby/aggregation 수행
- 처리 결과를 ECharts chart config로 변환

**Non-Goals:**
- LLM이 직접 ECharts JSON 생성 (샘플 기반이라 부정확)
- 복잡한 다단계 집계 (multi-stage aggregation)

## Decisions

### 1. LLM 응답 파싱 방식

**선택**: LLM이 JSON 형태의 분석 intent를 응답에 포함

```json
{
  "analysis_type": "group_by",
  "group_by": "학과",
  "value": "평점",
  "agg_func": "mean",
  "chart_type": "bar"
}
```

**이유**: 
- LLM이 직접 chart config를 생성하는 것보다 정확
- pandas로 실제 데이터 처리 가능
- 파싱이 간단하고 명확

### 2. pandas 처리 로직

**선택**: 백엔드에서 pandas로 groupby/aggregation 실행

```python
result = df.groupby('학과')['평점'].mean()
```

**이유**:
- 실제 CSV 데이터 전체 사용 가능
- DuckDB 설치 시 환경 오류가 발생하여 pandas로 대체 결정
- groupby/aggregation으로 bar, line, pie, scatter, heatmap 등 모든 ECharts 차트 타입 지원 가능

### 3. LLM 프롬프트 구조

**선택**: CSV 헤더 + 샘플 10개 전송 → 분석 intent 요청

**이유**:
- 600라인 전체 전송은 비효율적
- 10개 샘플이면 패턴 파악 가능
- LLM이 분석 방법 결정에 충분한 정보

## Risks / Trade-offs

- [Risk] LLM 응답 파싱 실패 시 chart 안 표시
  - → Mitigation: 파싱 실패 시 fallback으로 기존 방식 유지
- [Risk] pandas groupby 실패 시
  - → Mitigation: 예외 처리, graph: null 반환
- [Trade-off] 샘플 10개로 분석 결정 → 전체 데이터와 다를 수 있음
  - → Mitigation: pandas 처리 시 전체 데이터 사용

## Open Questions

1. LLM이 분석 intent 대신 직접 chart config 생성하는 방식은?
2. 복잡한 분석 (복수 컬럼 groupby, multi-stage aggregation) 지원 여부
3. 분석 intent에 포함할 필드 확장 (정렬, 필터링 등)
