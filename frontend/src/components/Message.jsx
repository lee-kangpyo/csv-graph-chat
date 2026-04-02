import ReactMarkdown from 'react-markdown'
import ActionChips from './ActionChips'

function Message({ role, content, suggestions, onShowToast }) {
  const isAI = role === 'assistant' || role === 'ai'
  
  const markdownStyles = {
    h1: 'text-2xl font-bold mt-4 mb-2 text-gray-800 dark:text-gray-100',
    h2: 'text-xl font-semibold mt-3 mb-2 text-gray-800 dark:text-gray-100',
    h3: 'text-lg font-medium mt-2 mb-1 text-gray-700 dark:text-gray-200',
    p: 'mb-2 text-gray-700 dark:text-gray-300 leading-relaxed',
    ul: 'list-disc ml-5 mb-2 space-y-1 text-gray-700 dark:text-gray-300',
    ol: 'list-decimal ml-5 mb-2 space-y-1 text-gray-700 dark:text-gray-300',
    li: 'ml-2',
    code: 'bg-gray-200 dark:bg-gray-700 px-1 py-0.5 rounded text-sm font-mono text-gray-800 dark:text-gray-200',
    pre: 'bg-gray-200 dark:bg-gray-700 p-3 rounded-lg overflow-x-auto mb-2',
    'pre code': 'bg-transparent p-0 text-sm',
    a: 'text-purple-600 dark:text-purple-400 hover:underline',
    strong: 'font-bold text-gray-900 dark:text-gray-100',
    em: 'italic text-gray-600 dark:text-gray-400',
    blockquote: 'border-l-4 border-gray-400 dark:border-gray-600 pl-4 italic text-gray-600 dark:text-gray-400 mb-2',
    table: 'w-full border-collapse mb-2',
    th: 'border border-gray-300 dark:border-gray-600 px-3 py-2 bg-gray-100 dark:bg-gray-700 text-left',
    td: 'border border-gray-300 dark:border-gray-600 px-3 py-2',
  }

  return (
    <div className={`message ${isAI ? 'ai-message' : 'user-message'} mb-4`}>
      <div className={`p-3 rounded-lg ${isAI 
        ? 'bg-gray-100 dark:bg-gray-800 text-left' 
        : 'bg-purple-100 dark:bg-purple-900 text-right'
      }`}>
        {isAI ? (
          <ReactMarkdown
            components={{
              h1: ({ children }) => <h1 className={markdownStyles.h1}>{children}</h1>,
              h2: ({ children }) => <h2 className={markdownStyles.h2}>{children}</h2>,
              h3: ({ children }) => <h3 className={markdownStyles.h3}>{children}</h3>,
              p: ({ children }) => <p className={markdownStyles.p}>{children}</p>,
              ul: ({ children }) => <ul className={markdownStyles.ul}>{children}</ul>,
              ol: ({ children }) => <ol className={markdownStyles.ol}>{children}</ol>,
              li: ({ children }) => <li className={markdownStyles.li}>{children}</li>,
              code: ({ inline, children, ...props }) => {
                if (inline) {
                  return <code className={markdownStyles.code} {...props}>{children}</code>
                }
                return (
                  <pre className={markdownStyles.pre}>
                    <code className={markdownStyles['pre code']} {...props}>{children}</code>
                  </pre>
                )
              },
              a: ({ href, children }) => (
                <a href={href} className={markdownStyles.a} target="_blank" rel="noopener noreferrer">
                  {children}
                </a>
              ),
              strong: ({ children }) => <strong className={markdownStyles.strong}>{children}</strong>,
              em: ({ children }) => <em className={markdownStyles.em}>{children}</em>,
              blockquote: ({ children }) => <blockquote className={markdownStyles.blockquote}>{children}</blockquote>,
              table: ({ children }) => <table className={markdownStyles.table}>{children}</table>,
              th: ({ children }) => <th className={markdownStyles.th}>{children}</th>,
              td: ({ children }) => <td className={markdownStyles.td}>{children}</td>,
            }}
          >
            {content}
          </ReactMarkdown>
        ) : (
          <p className="text-gray-800 dark:text-gray-100">{content}</p>
        )}
        
        {isAI && suggestions && suggestions.length > 0 && (
          <ActionChips suggestions={suggestions} onShowToast={onShowToast} />
        )}
      </div>
    </div>
  )
}

export default Message
