function Message({ role, content }) {
  const isAI = role === 'assistant' || role === 'ai'
  
  return (
    <div className={`message ${isAI ? 'ai-message' : 'user-message'} mb-4`}>
      <div className={`p-3 rounded-lg ${isAI 
        ? 'bg-gray-100 dark:bg-gray-800 text-left' 
        : 'bg-purple-100 dark:bg-purple-900 text-right'
      }`}>
        {content}
      </div>
    </div>
  )
}

export default Message
