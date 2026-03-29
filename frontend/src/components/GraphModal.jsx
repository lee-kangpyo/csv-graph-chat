import { useEffect, useRef } from 'react'
import * as echarts from 'echarts'

function GraphModal({ isOpen, onClose, graphConfig, userQuestion }) {
  const containerRef = useRef(null)
  const chartRef = useRef(null)
  const modalRef = useRef(null)

  useEffect(() => {
    if (!containerRef.current || !graphConfig || typeof graphConfig !== 'object' || Array.isArray(graphConfig)) return

    if (chartRef.current) {
      chartRef.current.dispose()
    }

    chartRef.current = echarts.init(containerRef.current)
    chartRef.current.setOption(graphConfig)

    const handleResize = () => {
      chartRef.current?.resize()
    }
    window.addEventListener('resize', handleResize)

    return () => {
      window.removeEventListener('resize', handleResize)
      chartRef.current?.dispose()
    }
  }, [graphConfig])

  useEffect(() => {
    const handleEsc = (e) => {
      if (e.key === 'Escape' && isOpen) {
        onClose()
      }
    }

    if (isOpen) {
      document.addEventListener('keydown', handleEsc)
      document.body.style.overflow = 'hidden'
    }

    return () => {
      document.removeEventListener('keydown', handleEsc)
      document.body.style.overflow = 'unset'
    }
  }, [isOpen, onClose])

  if (!isOpen || !graphConfig) return null

  const handleOverlayClick = (e) => {
    if (e.target === e.currentTarget || e.target === modalRef.current) {
      onClose()
    }
  }

  return (
    <div 
      className="fixed inset-0 bg-black bg-opacity-50 z-[1000] flex items-center justify-center"
      onClick={handleOverlayClick}
    >
      <div 
        ref={modalRef}
        className="bg-white dark:bg-gray-800 rounded-lg shadow-2xl flex flex-col"
        style={{ width: '80vw', height: '80vh', maxWidth: 'calc(100vw - 2rem)', maxHeight: 'calc(100vh - 2rem)' }}
      >
        <div className="flex items-start justify-between p-4 border-b border-gray-200 dark:border-gray-700">
          <div className="flex-1 pr-8">
            <h3 className="text-base font-medium text-gray-900 dark:text-white leading-snug">
              {userQuestion || 'Graph'}
            </h3>
          </div>
          <button
            onClick={onClose}
            className="p-2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-200 transition-colors flex-shrink-0"
            title="Close"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <div className="flex-1 p-4 overflow-hidden">
          <div ref={containerRef} style={{ width: '100%', height: '100%' }}></div>
        </div>
      </div>
    </div>
  )
}

export default GraphModal
