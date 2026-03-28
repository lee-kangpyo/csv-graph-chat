import { useEffect, useRef } from 'react'
import { Chart } from 'chart.js/auto'

function GraphView({ config }) {
  const canvasRef = useRef(null)
  const chartRef = useRef(null)

  useEffect(() => {
    if (!canvasRef.current || !config) return

    if (chartRef.current) {
      chartRef.current.destroy()
    }

    chartRef.current = new Chart(canvasRef.current, config)

    return () => {
      if (chartRef.current) {
        chartRef.current.destroy()
      }
    }
  }, [config])

  if (!config) return null

  return (
    <div className="p-4">
      <canvas ref={canvasRef}></canvas>
    </div>
  )
}

export default GraphView
