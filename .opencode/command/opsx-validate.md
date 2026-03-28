# OpenSpec Implementation Validator Command

스펙 대비 코드 구현을 검증하고 테스트를 실행합니다.

## 사용법

```
/openspec-validate [스펙명]
```

## 예시

```
/openspec-validate csv-upload-analysis
/openspec-validate ai-graph-conversation
/openspec-validate chart-rendering
/openspec-validate graph-basket
```

## 출력

구현 검증 결과를 표준 형식으로 출력:
- 구현율 (%)
- 기능별 검증 표
- 테스트 실행 결과
- 발견된 갭
- 권장 조치

## 권한

openspec 스펙 디렉토리 및 backend/src 디렉토리 읽기 권한 필요.
