const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export const createSSEStream = (message, csvMetadata = null, onMessage, onDone, onError) => {
  const eventSource = new EventSource(`${API_BASE}/api/chat/stream`)
  
  eventSource.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data)
      if (data.content) {
        onMessage(data.content)
      }
    } catch (err) {
      console.error('SSE parse error:', err)
    }
  }
  
  eventSource.onerror = (err) => {
    console.error('SSE error:', err)
    onError?.(err)
    eventSource.close()
  }
  
  eventSource.addEventListener('done', () => {
    onDone?.()
    eventSource.close()
  })
  
  fetch(`${API_BASE}/api/chat/stream`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ message, csv_metadata: csvMetadata }),
  })
  
  return eventSource
}

export const sendChatMessage = async (message, csvMetadata = null) => {
  const response = await fetch(`${API_BASE}/api/chat/stream`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ message, csv_metadata: csvMetadata }),
  })
  
  return response.body
}
