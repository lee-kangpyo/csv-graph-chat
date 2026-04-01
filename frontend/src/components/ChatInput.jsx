import { useState, useRef } from 'react'
import { uploadCSV } from '../api/csvApi'
import { createBasket } from '../api/basketApi'
import useCSVStore from '../stores/csvStore'
import useChatStore from '../stores/chatStore'
import useBasketStore from '../stores/basketStore'

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const CHART_KEYWORDS = ["차트", "그래프", "그려", "시각화", "chart", "graph", "plot", "visualize"]

function detectChartRequest(message) {
  const messageLower = message.toLowerCase()
  return CHART_KEYWORDS.some(keyword => messageLower.includes(keyword))
}

function ChatInput({ onShowToast }) {
  const [input, setInput] = useState('')
  const [uploading, setUploading] = useState(false)
  const [sending, setSending] = useState(false)
  const fileInputRef = useRef(null)
  const setCSVData = useCSVStore((state) => state.setCSVData)
  const addMessage = useChatStore((state) => state.addMessage)
  const setLoading = useChatStore((state) => state.setLoading)
  const addItem = useBasketStore((state) => state.addItem)
  const removeItem = useBasketStore((state) => state.removeItem)

  const generateGraphName = (question) => {
    if (!question || question.trim() === '') {
      return `Graph ${Date.now()}`
    }

    let name = question.trim()

    name = name.replace(/[^\w\s-]/g, '')

    if (name.length > 50) {
      name = name.substring(0, 47) + '...'
    }

    if (!name || name.trim() === '') {
      return `Graph ${Date.now()}`
    }

    return name
  }

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
    const requestId = `req-${Date.now()}`
    setInput('')
    setSending(true)
    setLoading(true)
    
    addMessage('user', userMessage)
    addMessage('ai', '...')
    
    const csvData = useCSVStore.getState()
    const csvMetadata = csvData.fileId ? {
      file_id: csvData.fileId,
      columns: csvData.columns,
      row_count: csvData.rowCount
    } : null

    const isChartRequest = detectChartRequest(userMessage)
    let placeholderId = null
    const graphName = generateGraphName(userMessage)

    if (isChartRequest) {
      placeholderId = `loading-${Date.now()}`
      addItem({
        id: placeholderId,
        name: graphName,
        graph_config: null,
        question: userMessage,
        isLoading: true
      })
    }

    const ssePromise = new Promise((resolve, reject) => {
      fetch(`${API_BASE}/api/chat/stream`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          message: userMessage,
          csv_metadata: csvMetadata,
          request_id: requestId
        }),
      })
      .then(response => {
        if (!response.ok) throw new Error('SSE failed')
        const reader = response.body.getReader()
        const decoder = new TextDecoder()
        let buffer = ''

        const read = () => {
          reader.read().then(({ done, value }) => {
            if (done) {
              resolve()
              return
            }
            buffer += decoder.decode(value, { stream: true })
            const lines = buffer.split('\n')
            buffer = lines.pop() || ''
            
            for (const line of lines) {
              if (line.startsWith('data: ')) {
                try {
                  const data = JSON.parse(line.slice(6))
                  if (data.content) {
                    useChatStore.setState((state) => {
                      const messages = [...state.messages]
                      const lastMessage = messages[messages.length - 1]
                      if (lastMessage && lastMessage.role === 'ai') {
                        messages[messages.length - 1] = { ...lastMessage, content: (lastMessage.content || '') + data.content }
                      }
                      return { messages }
                    })
                  }
                } catch (e) {}
              }
            }
            read()
          })
        }
        read()
      })
      .catch(reject)
    })

    const chartPromise = isChartRequest ? fetch(`${API_BASE}/api/chart/generate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message: userMessage,
        csv_metadata: csvMetadata,
        request_id: requestId
      }),
    }).then(async response => {
      if (!response.ok) throw new Error('Chart generation failed')
      return response.json()
    }) : Promise.resolve({ graph: null })

    try {
      await ssePromise
      const chartResult = await chartPromise
      
      if (isChartRequest && chartResult.graph && typeof chartResult.graph === 'object') {
        if (placeholderId) removeItem(placeholderId)
        createBasket(graphName, chartResult.graph, userMessage)
          .then((response) => {
            addItem({
              id: response.id,
              name: response.name,
              graph_config: response.graph_config,
              question: userMessage
            })
          })
          .catch((err) => {
            onShowToast('Failed to save graph to Basket', 'error')
          })
      } else if (placeholderId) {
        removeItem(placeholderId)
      }
    } catch (err) {
      if (placeholderId) removeItem(placeholderId)
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
