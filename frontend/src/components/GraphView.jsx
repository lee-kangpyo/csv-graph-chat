import { useEffect, useRef } from 'react'
import * as echarts from 'echarts'

function GraphView({ config }) {
  const containerRef = useRef(null)
  const chartRef = useRef(null)

  useEffect(() => {
    if (!containerRef.current || !config || typeof config !== 'object' || Array.isArray(config)) return

    if (chartRef.current) {
      chartRef.current.dispose()
    }

    chartRef.current = echarts.init(containerRef.current)
    chartRef.current.setOption(config)

    const handleResize = () => {
      chartRef.current?.resize()
    }
    window.addEventListener('resize', handleResize)

    return () => {
      window.removeEventListener('resize', handleResize)
      chartRef.current?.dispose()
    }
  }, [config])

  if (!config) return null

  return (
    <div className="p-4">
      <div ref={containerRef} style={{ width: '100%', height: '400px' }}></div>
    </div>
  )
}

export default GraphView