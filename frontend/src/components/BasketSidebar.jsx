import { useState, useEffect } from 'react'
import BasketItem from './BasketItem'
import axios from 'axios'

function BasketSidebar({ onShowToast }) {
  const [items, setItems] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetchBaskets()
  }, [])

  const fetchBaskets = async () => {
    try {
      const response = await axios.get('/api/basket/')
      setItems(Array.isArray(response.data) ? response.data : [])
      setError(null)
    } catch (err) {
      console.error('Failed to fetch baskets:', err)
      setError('백엔드 서버가 실행되지 않았습니다. backend 폴더에서 "uvicorn main:app --reload"를 실행해주세요.')
    }
  }

  const handleDelete = async (id) => {
    try {
      await axios.delete(`/api/basket/${id}`)
      setItems(items.filter(item => item.id !== id))
      onShowToast('Graph deleted from basket', 'success')
    } catch (err) {
      onShowToast('Failed to delete graph', 'error')
    }
  }

  const handleDownload = async () => {
    if (items.length === 0) {
      onShowToast('No graphs to download', 'error')
      return
    }

    try {
      const htmlContent = generateHTMLDownload(items)
      const blob = new Blob([htmlContent], { type: 'text/html' })
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = 'graphs.html'
      a.click()
      URL.revokeObjectURL(url)
      onShowToast('Download started', 'success')
    } catch (err) {
      onShowToast('Failed to download', 'error')
    }
  }

  const generateHTMLDownload = (graphs) => {
    const chartsHTML = graphs.map((graph, idx) => `
      <div class="chart-container">
        <h3>${graph.name}</h3>
        <canvas id="chart${idx}"></canvas>
        <script>
          new Chart(document.getElementById('chart${idx}'), ${JSON.stringify(graph.graph_config)});
        </script>
      </div>
    `).join('')

    return `
      <!DOCTYPE html>
      <html>
      <head>
        <title>CSV Graph Chat - Graphs</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
          body { font-family: system-ui, sans-serif; padding: 20px; }
          .chart-container { margin-bottom: 40px; border: 1px solid #ddd; padding: 20px; border-radius: 8px; }
          h3 { margin-top: 0; }
        </style>
      </head>
      <body>
        <h1>My Graphs</h1>
        ${chartsHTML}
      </body>
      </html>
    `
  }

  return (
    <aside className="w-64 border-r border-gray-200 dark:border-gray-700 flex flex-col bg-gray-50 dark:bg-gray-900">
      <div className="p-4 border-b border-gray-200 dark:border-gray-700">
        <h2 className="text-lg font-semibold">Graph Basket</h2>
        <p className="text-sm text-gray-500">{items.length} graphs</p>
      </div>
      
      <div className="flex-1 overflow-y-auto p-2">
        {error ? (
          <div className="text-center text-red-500 p-4">
            <p className="text-sm mb-2 font-medium">⚠️ 연결 오류</p>
            <p className="text-xs text-gray-600 dark:text-gray-400">{error}</p>
          </div>
        ) : items.length === 0 ? (
          <div className="text-center text-gray-500 p-4">
            <p className="text-sm mb-2">Your basket is empty</p>
            <p className="text-xs">Save graphs from chat to see them here</p>
          </div>
        ) : (
          items.map(item => (
            <BasketItem
              key={item.id}
              item={item}
              onDelete={handleDelete}
            />
          ))
        )}
      </div>
      
      {items.length > 0 && (
        <div className="p-4 border-t border-gray-200 dark:border-gray-700">
          <button
            onClick={handleDownload}
            className="w-full px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700"
          >
            Download All (HTML)
          </button>
        </div>
      )}
    </aside>
  )
}

export default BasketSidebar
