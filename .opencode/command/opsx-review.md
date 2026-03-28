# OpenSpec Reviewer Command

openspec에 정의된 스펙을 검토합니다.

## 사용법

```
/openspec-reviewer [스펙명]
```

## 예시

```
/openspec-reviewer csv-upload-analysis
/openspec-reviewer ai-graph-conversation
/openspec-reviewer chart-rendering
/openspec-reviewer graph-basket
```

## 출력

스펙 검토 결과를 표준 형식으로 출력:
- 완전성 점수 (10점 만점)
- 발견된 이슈 (중요/보통/미비)
- 권장 수정사항
- 종합 의견

## 권한

모든 openspec 스펙 디렉토리 읽기 권한 필요.
