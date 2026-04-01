## 1. Dependencies

- [x] 1.1 `cd frontend && npm install react-markdown` 실행 (package.json에 추가됨)

## 2. Message.jsx 마크다운 렌더링

- [x] 2.1 `Message.jsx`에 `import ReactMarkdown from 'react-markdown'` 추가
- [x] 2.2 AI 메시지(`isAI === true`)일 때 `<ReactMarkdown>{content}</ReactMarkdown>` 사용
- [x] 2.3 user 메시지는 기존처럼 `<p>{content}</p>` 유지

## 3. 마크다운 스타일링

- [x] 3.1 Tailwind 클래스로 마크다운 요소 스타일링
  - h1-h3: 크기, 폰트 두께 ✓
  - code: 인라인 배경색, 블록 좌우 패딩 ✓
  - ul/ol: 들여쓰기, 불릿/번호 스타일 ✓
  - a: 링크 색상 ✓
  - strong, em: 강조 스타일 ✓

## 4. 검증 (수동)

- [x] 4.1 AI 응답이 마크다운으로 올바르게 렌더링되는지 확인
- [x] 4.2 코드 블록이 이쁘게 표시되는지 확인
- [x] 4.3 목록이 들여쓰기로 표시되는지 확인
- [x] 4.4 다크모드에서 가독성 확인

