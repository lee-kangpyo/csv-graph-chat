import { useEffect, useRef } from 'react'
import Message from './Message'
import useChatStore from '../stores/chatStore'
import useCSVStore from '../stores/csvStore'

function ChatArea({ currentGraph, onGraphGenerated, onShowToast }) {
  const messagesEndRef = useRef(null)
  const messages = useChatStore((state) => state.messages)
  const isLoading = useChatStore((state) => state.isLoading)
  const csvData = useCSVStore((state) => state.fileId)
  
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const showEmptyState = messages.length === 0 && !isLoading

  return (
    <div className="flex-1 overflow-y-auto p-4">
      <div className="max-w-3xl mx-auto">
        <div className="flex justify-end mb-2">
          <button
            onClick={() => window.location.href = '?test=1'}
            className="text-xs px-2 py-1 bg-gray-200 dark:bg-gray-700 rounded hover:bg-gray-300 dark:hover:bg-gray-600"
          >
            차트 테스트
          </button>
        </div>
        {showEmptyState && !csvData && (
          <div className="text-center text-gray-500 dark:text-gray-400 mt-8">
            <p className="text-lg mb-2">Upload a CSV file to get started</p>
            <p className="text-sm">Click the + button below to upload your file</p>
          </div>
        )}
        
        {showEmptyState && csvData && (
          <div className="text-center text-gray-500 dark:text-gray-400 mt-8">
            <p className="text-lg mb-2">Ready to analyze your data</p>
            <p className="text-sm">Ask me anything about your CSV data!</p>
          </div>
        )}
        
        {isLoading && (
          <div className="text-center text-gray-500 dark:text-gray-400 py-4">
            <p className="animate-pulse">AI is thinking...</p>
          </div>
        )}
        
        {messages.map((msg, idx) => (
          <Message key={idx} role={msg.role} content={msg.content} />
        ))}
        
        <div ref={messagesEndRef} />
      </div>
    </div>
  )
}

export default ChatArea
