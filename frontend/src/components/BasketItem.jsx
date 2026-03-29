import { useEffect, useRef, useState } from 'react'
import * as echarts from 'echarts'

function BasketItem({ item, onDelete, onGraphClick }) {
  const graphType = item.graph_config?.type || 'unknown'
  const previewRef = useRef(null)
  const chartRef = useRef(null)
  const [isLoaded, setIsLoaded] = useState(false)

  useEffect(() => {
    if (!previewRef.current || !item.graph_config || typeof item.graph_config !== 'object' || Array.isArray(item.graph_config)) return

    setIsLoaded(false)

    if (chartRef.current) {
      chartRef.current.dispose()
    }

    const miniChart = echarts.init(previewRef.current, null, { renderer: 'canvas' })
    const scaledConfig = { ...item.graph_config }

    scaledConfig.grid = { ...scaledConfig.grid, top: 5, bottom: 5, left: 5, right: 5 }
    scaledConfig.title = undefined
    scaledConfig.legend = undefined

    miniChart.setOption(scaledConfig)
    chartRef.current = miniChart
    setIsLoaded(true)

    return () => {
      chartRef.current?.dispose()
    }
  }, [item.graph_config])

  const getTypeIcon = () => {
    switch (graphType) {
      case 'line': return '📈'
      case 'bar': return '📊'
      case 'doughnut': return '🍩'
      case 'scatter': return '⚬'
      default: return '📈'
    }
  }

  const handleClick = () => {
    onGraphClick?.(item)
  }

  return (
    <div
      onClick={handleClick}
      className="p-3 mb-2 bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 cursor-pointer hover:border-purple-400 dark:hover:border-purple-500 transition-colors"
    >
      <div className="flex gap-3">
        <div className="flex-shrink-0">
          <div ref={previewRef} style={{ width: '150px', height: '100px' }} className={!isLoaded ? 'bg-gray-100 dark:bg-gray-700 animate-pulse' : ''}></div>
        </div>
        <div className="flex-1 min-w-0">
          <p className="font-medium text-sm truncate mb-1">{item.name}</p>
          <p className="text-xs text-gray-500">{graphType}</p>
        </div>
        <button
          onClick={(e) => {
            e.stopPropagation()
            onDelete(item.id)
          }}
          className="p-1 text-gray-400 hover:text-red-500 transition-colors flex-shrink-0"
          title="Delete"
        >
          ✕
        </button>
      </div>
    </div>
  )
}

export default BasketItem
