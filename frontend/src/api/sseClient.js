const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000'
const SSE_TIMEOUT_MS = 30000

export const createSSEStream = (message, csvMetadata = null, onMessage, onStatus, onDone, onError, onGraph) => {
  let timeoutId = null
  let aborted = false

  const cleanup = () => {
    if (timeoutId) clearTimeout(timeoutId)
  }

  timeoutId = setTimeout(() => {
    if (!aborted) {
      aborted = true
      cleanup()
      onError?.({ type: 'timeout', message: 'AI 응답 시간이 초과되었습니다. 다시 시도해주세요.' })
    }
  }, SSE_TIMEOUT_MS)

  fetch(`${API_BASE}/api/chat/stream`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ message, csv_metadata: csvMetadata }),
  })
    .then(response => {
      if (!response.ok) {
        throw new Error(`HTTP error: ${response.status}`)
      }
      const reader = response.body.getReader()
      const decoder = new TextDecoder()
      let buffer = ''

      const readStream = () => {
        reader.read().then(({ done, value }) => {
          if (done || aborted) {
            cleanup()
            onDone?.()
            return
          }

          buffer += decoder.decode(value, { stream: true })
          const lines = buffer.split('\n')
          buffer = lines.pop() || ''

          for (const line of lines) {
            if (line.startsWith('event:')) {
              continue
            }
            if (line.startsWith('data:')) {
              const dataStr = line.slice(5).trim()
              try {
                const data = JSON.parse(dataStr)
                if (data.content) {
                  onMessage(data.content)
                }
                if (data.graph && typeof data.graph === 'object') {
                  onGraph?.(data.graph)
                }
                if (data.status) {
                  onStatus?.(data.status)
                }
              } catch {
                // ignore parse errors for non-JSON data
              }
            }
          }

          readStream()
        }).catch(err => {
          cleanup()
          if (!aborted) {
            onError?.(err)
          }
        })
      }

      readStream()
    })
    .catch(err => {
      cleanup()
      if (!aborted) {
        onError?.(err)
      }
    })

  return {
    abort: () => {
      aborted = true
      cleanup()
    }
  }
}