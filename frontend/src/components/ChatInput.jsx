import { useState, useRef } from 'react'
import { uploadCSV } from '../api/csvApi'
import { createBasket } from '../api/basketApi'
import useCSVStore from '../stores/csvStore'
import useChatStore from '../stores/chatStore'
import useBasketStore from '../stores/basketStore'

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000'


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
    
    const userMessageLower = userMessage.toLowerCase()
    const BATCH_KEYWORDS = ["다 그려", "전부 그려", "모두 그려", "다 만들어", "전부 만들어"]
    const isBatchRequest = BATCH_KEYWORDS.some(k => userMessageLower.includes(k))
    const currentMessages = useChatStore.getState().messages
    const lastMsg = currentMessages.length > 0 ? currentMessages[currentMessages.length - 1] : null
    let suggestionsToBatch = []

    if (isBatchRequest && lastMsg && lastMsg.role === 'ai' && lastMsg.suggestions?.length > 0) {
      suggestionsToBatch = lastMsg.suggestions
    }

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

    try {
      const response = await fetch(`${API_BASE}/api/chat/stream`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          message: userMessage,
          csv_metadata: csvMetadata,
          request_id: requestId
        }),
      })

      if (!response.ok) throw new Error('SSE failed')
      
      const reader = response.body.getReader()
      const decoder = new TextDecoder()
      let buffer = ''
      let fullText = ''

      while (true) {
        const { done, value } = await reader.read()
        if (done) break
        
        buffer += decoder.decode(value, { stream: true })
        const lines = buffer.split('\n')
        buffer = lines.pop() || ''
        
        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const data = JSON.parse(line.slice(6))
              if (data.content) {
                fullText += data.content
                
                let cleanText = fullText
                const currentSuggestions = []
                
                cleanText = cleanText.replace(/\[SUGGESTION:(\{[\s\S]*?\})\]/g, (match, jsonStr) => {
                  try {
                    const parsed = JSON.parse(jsonStr)
                    currentSuggestions.push(parsed)
                    return ''
                  } catch {
                    return match
                  }
                })
                
                let displayText = cleanText
                const unclosedMatch = displayText.match(/\[[^\]]*$/)
                if (unclosedMatch) {
                  const tail = unclosedMatch[0]
                  if ("[SUGGESTION:".startsWith(tail.substring(0, 12)) || tail.startsWith("[SUGGESTION:")) {
                    displayText = displayText.substring(0, unclosedMatch.index)
                  }
                }

                useChatStore.setState((state) => {
                  const messages = [...state.messages]
                  const lastMessage = messages[messages.length - 1]
                  if (lastMessage && lastMessage.role === 'ai') {
                    messages[messages.length - 1] = { 
                      ...lastMessage, 
                      content: displayText,
                      suggestions: currentSuggestions
                    }
                  }
                  return { messages }
                })
              }
            } catch {
              // JSON parse error - ignore
            }
          }
        }
      }

      if (suggestionsToBatch.length > 0) {
        onShowToast(`Starting batch generation for ${suggestionsToBatch.length} charts...`, 'success')
        for (let i = 0; i < suggestionsToBatch.length; i++) {
          const sug = suggestionsToBatch[i]
          const placeholderId = `loading-${Date.now()}-${i}`
          const graphName = sug.title || `Graph ${Date.now()}`
          const question = sug.description || sug.title
          
          addItem({
            id: placeholderId,
            name: graphName,
            graph_config: null,
            question: question,
            isLoading: true
          })
          
          try {
            onShowToast(`${i+1}/${suggestionsToBatch.length} 차트 생성 중...`, 'info')
            const chartResponse = await fetch(`${API_BASE}/api/chart/generate`, {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({
                message: `${sug.chart_type} 차트로 그려줘: ${sug.title}`,
                csv_metadata: csvMetadata,
                request_id: requestId + `-batch-${i}`
              })
            })
            
            if (!chartResponse.ok) throw new Error('Chart generation failed')
            const chartResult = await chartResponse.json()
            
            if (chartResult.graph) {
              removeItem(placeholderId)
              try {
                 const createResult = await createBasket(graphName, chartResult.graph, question)
                 addItem({
                   id: createResult.id,
                   name: createResult.name,
                   graph_config: createResult.graph_config,
                   question: question
                 })
                 onShowToast(`${i+1}/${suggestionsToBatch.length} 차트 생성 완료`, 'success')
              } catch {
                 removeItem(placeholderId)
                 onShowToast(`Failed to save chart ${i+1} to basket`, 'error')
              }
            } else {
               throw new Error('Graph generation returned null')
            }
          } catch {
             removeItem(placeholderId)
             onShowToast(`Failed to generate chart ${i+1}`, 'error')
          }
        }
        onShowToast(`모든 차트 생성이 완료되었습니다.`, 'success')
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
