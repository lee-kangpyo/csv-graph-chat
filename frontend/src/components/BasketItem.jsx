function BasketItem({ item, onDelete }) {
  const graphType = item.graph_config?.type || 'unknown'
  
  const getTypeIcon = () => {
    switch (graphType) {
      case 'line': return '📈'
      case 'bar': return '📊'
      case 'doughnut': return '🍩'
      case 'scatter': return '⚬'
      default: return '📈'
    }
  }

  return (
    <div className="p-3 mb-2 bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700">
      <div className="flex items-start gap-2">
        <span className="text-xl">{getTypeIcon()}</span>
        <div className="flex-1 min-w-0">
          <p className="font-medium text-sm truncate">{item.name}</p>
          <p className="text-xs text-gray-500">{graphType}</p>
        </div>
        <button
          onClick={() => onDelete(item.id)}
          className="p-1 text-gray-400 hover:text-red-500 transition-colors"
          title="Delete"
        >
          ✕
        </button>
      </div>
    </div>
  )
}

export default BasketItem
