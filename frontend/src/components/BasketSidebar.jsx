import { useEffect } from 'react'
import BasketItem from './BasketItem'
import axios from 'axios'
import useBasketStore from '../stores/basketStore'
import { downloadHTML } from '../utils/htmlDownload'

function BasketSidebar({ onShowToast, onGraphClick }) {
  const { items, setItems, removeItem } = useBasketStore()
  const error = null

  useEffect(() => {
    const fetchBaskets = async () => {
      try {
        const response = await axios.get('/api/basket/')
        setItems(Array.isArray(response.data) ? response.data : [])
      } catch {
        onShowToast?.('Failed to load baskets', 'error')
      }
    }
    fetchBaskets()
  }, [onShowToast, setItems])

  const handleDelete = async (id) => {
    try {
      await axios.delete(`/api/basket/${id}`)
      removeItem(id)
      onShowToast?.('Graph deleted from basket', 'success')
    } catch {
      onShowToast?.('Failed to delete graph', 'error')
    }
  }

  const handleDownload = async () => {
    if (items.length === 0) {
      onShowToast?.('No graphs to download', 'error')
      return
    }

    try {
      downloadHTML(items)
      onShowToast?.('Download started', 'success')
    } catch {
      onShowToast?.('Failed to download', 'error')
    }
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
              onGraphClick={onGraphClick}
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