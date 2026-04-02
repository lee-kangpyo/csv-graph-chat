import { useState } from 'react'
import { createBasket } from '../api/basketApi'
import useBasketStore from '../stores/basketStore'
import useCSVStore from '../stores/csvStore'

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000'

function ActionChips({ suggestions, onShowToast }) {
  const [clickedChips, setClickedChips] = useState(new Set())
  const addItem = useBasketStore((state) => state.addItem)
  const removeItem = useBasketStore((state) => state.removeItem)
  const csvData = useCSVStore((state) => state)

  if (!suggestions || suggestions.length === 0) return null

  const handleChipClick = async (suggestion, index) => {
    if (clickedChips.has(index)) return
    
    setClickedChips(prev => new Set([...prev, index]))
    
    const placeholderId = `loading-${Date.now()}`
    const graphName = suggestion.title || `Graph ${Date.now()}`
    const question = suggestion.description || suggestion.title

    addItem({
      id: placeholderId,
      name: graphName,
      graph_config: null,
      question: question,
      isLoading: true
    })

    const csvMetadata = csvData.fileId ? {
      file_id: csvData.fileId,
      columns: csvData.columns,
      row_count: csvData.rowCount
    } : null

    try {
      const response = await fetch(`${API_BASE}/api/chart/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: `${suggestion.chart_type} 차트로 그려줘: ${suggestion.title}`,
          csv_metadata: csvMetadata,
          request_id: `req-${Date.now()}`
        })
      })
      
      if (!response.ok) throw new Error('Failed to generate chart')
      const result = await response.json()
      
      if (result.graph) {
        removeItem(placeholderId)
        let createResult = null
        try {
          createResult = await createBasket(graphName, result.graph, question)
          addItem({
            id: createResult.id,
            name: createResult.name,
            graph_config: createResult.graph_config,
            question: question
          })
          onShowToast('Chart generated and saved to basket', 'success')
        } catch {
          removeItem(createResult?.id || placeholderId)
          onShowToast('Failed to save to basket', 'error')
          setClickedChips(prev => {
            const next = new Set([...prev])
            next.delete(index)
            return next
          })
        }
      } else {
        throw new Error('Graph generation returned null')
      }
    } catch (err) {
      removeItem(placeholderId)
      onShowToast(err.message || 'Chart generation failed', 'error')
      setClickedChips(prev => {
        const next = new Set([...prev])
        next.delete(index)
        return next
      })
    }
  }

  return (
    <div className="flex flex-wrap gap-2 mt-3 pt-3 border-t border-gray-200 dark:border-gray-700">
      {suggestions.map((sug, i) => {
        const isClicked = clickedChips.has(i)
        return (
          <button
            key={i}
            onClick={() => handleChipClick(sug, i)}
            disabled={isClicked}
            className={`text-xs px-3 py-1.5 rounded-full border transition-colors flex items-center gap-1.5 shadow-sm
              ${isClicked 
                ? 'bg-gray-100 dark:bg-gray-800 text-gray-400 dark:text-gray-500 border-gray-200 dark:border-gray-700 cursor-not-allowed' 
                : 'bg-white dark:bg-gray-800 text-purple-600 dark:text-purple-400 border-purple-200 dark:border-purple-800 hover:bg-purple-50 dark:hover:bg-purple-900/30 font-medium'
              }`}
            title={sug.description}
          >
            <span className="opacity-80">📈</span>
            <span>{sug.title}</span>
            <span className="opacity-40 font-normal">({sug.chart_type})</span>
          </button>
        )
      })}
    </div>
  )
}

export default ActionChips
