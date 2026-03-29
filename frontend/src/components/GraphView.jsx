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

  const chartType = config?.series?.[0]?.type || (config?.radar ? 'radar' : 'default')
  const isLargeChart = ['sankey', 'heatmap', 'radar', 'sunburst', 'boxplot'].includes(chartType)
  const chartHeight = isLargeChart ? '600px' : '400px'

  return (
    <div className="p-4">
      <div ref={containerRef} style={{ width: '100%', height: chartHeight }}></div>
    </div>
  )
}

export default GraphView