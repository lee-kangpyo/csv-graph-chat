import { useState, useRef } from 'react'
import { uploadCSV } from '../api/csvApi'
import useCSVStore from '../stores/csvStore'
import useChatStore from '../stores/chatStore'

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000'

function ChatInput({ onShowToast, onGraphGenerated }) {
  const [input, setInput] = useState('')
  const [uploading, setUploading] = useState(false)
  const [sending, setSending] = useState(false)
  const fileInputRef = useRef(null)
  const setCSVData = useCSVStore((state) => state.setCSVData)
  const addMessage = useChatStore((state) => state.addMessage)
  const setLoading = useChatStore((state) => state.setLoading)

  const handleFileSelect = async (e) => {
    const file = e.target.files?.[0]
    if (!file) return

    if (!file.name.endsWith('.csv')) {
      onShowToast('Please select a CSV file', 'error')
      return
    }

    if (file.size > 10 * 1024 * 1024) {
      onShowToast('File size exceeds 10MB limit', 'error')
      return
    }

    setUploading(true)
    
    try {
      const result = await uploadCSV(file)
      setCSVData(result)
      onShowToast('CSV file uploaded successfully', 'success')
    } catch (err) {
      const errorMessage = err.response?.data?.detail || err.message || 'Upload failed'
      onShowToast(errorMessage, 'error')
    } finally {
      setUploading(false)
      if (fileInputRef.current) {
        fileInputRef.current.value = ''
      }
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!input.trim() || sending) return
    
    const userMessage = input.trim()
    setInput('')
    setSending(true)
    setLoading(true)
    
    addMessage('user', userMessage)
    addMessage('ai', '...')
    
    try {
      const csvData = useCSVStore.getState()
      const response = await fetch(`${API_BASE}/api/chat/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          message: userMessage,
          csv_metadata: csvData.fileId ? {
            file_id: csvData.fileId,
            columns: csvData.columns,
            row_count: csvData.rowCount
          } : null
        }),
      })
      
      if (!response.ok) {
        throw new Error('Failed to get response')
      }
      
      const data = await response.json()
      
      useChatStore.setState((state) => {
        const messages = [...state.messages]
        const lastMessage = messages[messages.length - 1]
        if (lastMessage && lastMessage.role === 'ai') {
          messages[messages.length - 1] = { ...lastMessage, content: data.content || 'No response' }
        }
        return { messages }
      })

      if (data.graph && typeof data.graph === 'object') {
        onGraphGenerated?.(data.graph)
      }
    } catch (err) {
      onShowToast(err.message || 'Chat failed', 'error')
    } finally {
      setSending(false)
      setLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="border-t border-gray-200 dark:border-gray-700 p-4">
      <div className="flex gap-2 max-w-3xl mx-auto">
        <button
          type="button"
          onClick={() => fileInputRef.current?.click()}
          disabled={uploading}
          className="p-2 rounded-lg bg-gray-100 dark:bg-gray-800 hover:bg-gray-200 dark:hover:bg-gray-700 disabled:opacity-50"
          title="Upload CSV"
        >
          {uploading ? '...' : '+'}
        </button>
        
        <input
          ref={fileInputRef}
          type="file"
          accept=".csv"
          onChange={handleFileSelect}
          className="hidden"
        />
        
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask about your data..."
          disabled={sending}
          className="flex-1 p-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-purple-500 disabled:opacity-50"
        />
        
        <button
          type="submit"
          disabled={!input.trim() || sending}
          className="px-4 py-2 rounded-lg bg-purple-600 text-white hover:bg-purple-700 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {sending ? '...' : 'Send'}
        </button>
      </div>
    </form>
  )
}

export default ChatInput
