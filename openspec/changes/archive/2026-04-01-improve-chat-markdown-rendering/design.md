## Approach

### 1. Dependencies

`react-markdown` 설치:
```bash
cd frontend && npm install react-markdown
```

선택적: 코드 구문 강조를 위해 `react-syntax-highlighter` 설치 (나중에 추가 가능)

### 2. Message.jsx 수정

```jsx
import ReactMarkdown from 'react-markdown'

function Message({ role, content }) {
  const isAI = role === 'assistant' || role === 'ai'
  
  return (
    <div className={`message ${isAI ? 'ai-message' : 'user-message'} mb-4`}>
      <div className={`p-3 rounded-lg ${isAI 
        ? 'bg-gray-100 dark:bg-gray-800 text-left' 
        : 'bg-purple-100 dark:bg-purple-900 text-right'
      }`}>
        {isAI ? (
          <ReactMarkdown>{content}</ReactMarkdown>
        ) : (
          <p>{content}</p>
        )}
      </div>
    </div>
  )
}
```

### 3. 스타일링 고려사항

AI 메시지의 마크다운 스타일:
- `h1`, `h2`, `h3`: 크기 구분, 폰트 두께
- `code`: 인라인은 배경색, 블록은 좌우 패딩
- `ul`, `ol`: 들여쓰기, 불릿/번호 스타일
- `a`: 링크 색상, 밑줄
- `strong`, `em`: 적절한 강조

### 4. 구현 순서

1. `react-markdown` 설치
2. `Message.jsx` 기본 마크다운 렌더링 적용
3. 기본 Tailwind 스타일로 마크다운 요소 스타일링
4. (선택적) 코드 블록 구문 강조 추가

## Constraints

- 기존 다크모드 지원 유지
- 기존 user-message 스타일 유지
- 다른 컴포넌트에 영향 없음
