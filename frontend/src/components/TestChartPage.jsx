import { useState } from 'react'
import GraphView from './GraphView'

const presets = {
  bar: {
    title: { text: 'Bar Chart - 단과대학별 학생 수' },
    tooltip: { trigger: 'axis' },
    xAxis: {
      type: 'category',
      data: ['경영대학', '공과대학', '사회과학대학', '인문대학', '자연과학대학', '예술대학']
    },
    yAxis: { type: 'value' },
    series: [{
      type: 'bar',
      data: [120, 200, 150, 80, 70, 110]
    }]
  },
  line: {
    title: { text: 'Line Chart - 월별 추이' },
    tooltip: { trigger: 'axis' },
    xAxis: {
      type: 'category',
      data: ['1월', '2월', '3월', '4월', '5월', '6월']
    },
    yAxis: { type: 'value' },
    series: [{
      type: 'line',
      data: [820, 932, 901, 934, 1290, 1330]
    }]
  },
  pie: {
    title: { text: 'Pie Chart - 학사경고 비율' },
    tooltip: { trigger: 'item' },
    series: [{
      type: 'pie',
      radius: '50%',
      data: [
        { value: 500, name: '경고 없음' },
        { value: 150, name: '경고 1회' },
        { value: 50, name: '경고 2회' },
        { value: 16, name: '경고 3회 이상' }
      ]
    }]
  },
  scatter: {
    title: { text: 'Scatter Chart - 평점 상관관계' },
    tooltip: { trigger: 'item' },
    xAxis: { type: 'value', name: '전학기 평점' },
    yAxis: { type: 'value', name: '현재 평점' },
    series: [{
      type: 'scatter',
      data: [
        [1.5, 2.0], [2.0, 2.5], [3.0, 3.2], [3.5, 3.0], [4.0, 4.2],
        [2.5, 2.8], [3.2, 3.5], [1.8, 1.5], [3.8, 3.9], [2.2, 2.4]
      ]
    }]
  },
  boxplot: {
    title: { text: 'Boxplot - 단과대학별 GPA 분포' },
    tooltip: { trigger: 'axis' },
    xAxis: {
      type: 'category',
      data: ['경영대학', '공과대학', '사회과학대학', '인문대학', '자연과학대학']
    },
    yAxis: { type: 'value', name: 'GPA' },
    series: [{
      name: 'GPA',
      type: 'boxplot',
      data: [
        [0.5, 1.2, 2.1, 3.0, 4.0],
        [0.8, 1.5, 2.5, 3.3, 4.2],
        [0.3, 1.0, 1.8, 2.7, 3.8],
        [0.2, 0.9, 1.5, 2.4, 3.5],
        [0.6, 1.3, 2.2, 3.1, 4.1]
      ]
    }]
  },
  heatmap: {
    title: { text: 'Heatmap - 학년별 성적 분포' },
    tooltip: { trigger: 'item' },
    xAxis: {
      type: 'category',
      data: ['1학년', '2학년', '3학년', '4학년']
    },
    yAxis: {
      type: 'category',
      data: ['A', 'B', 'C', 'D', 'F']
    },
    visualMap: {
      min: 0,
      max: 50,
      calculable: true,
      orient: 'vertical',
      right: 10,
      top: 'center'
    },
    series: [{
      type: 'heatmap',
      data: [
        [0, 0, 45], [0, 1, 32], [0, 2, 15], [0, 3, 5], [0, 4, 3],
        [1, 0, 38], [1, 1, 28], [1, 2, 18], [1, 3, 8], [1, 4, 2],
        [2, 0, 30], [2, 1, 25], [2, 2, 20], [2, 3, 12], [2, 4, 3],
        [3, 0, 25], [3, 1, 22], [3, 2, 18], [3, 3, 15], [3, 4, 5]
      ]
    }]
  },
  sankey: {
    title: { text: 'Sankey - 학사경고 흐름' },
    tooltip: { trigger: 'item' },
    series: [{
      type: 'sankey',
      layout: 'none',
      emphasis: { focus: 'adjacency' },
      data: [
        { name: '입학' },
        { name: '경영대학' },
        { name: '공과대학' },
        { name: '사회과학대학' },
        { name: '졸업' },
        { name: '자연진급' },
        { name: '학사경고' },
        { name: '제적' }
      ],
      links: [
        { source: '입학', target: '경영대학', value: 100 },
        { source: '입학', target: '공과대학', value: 150 },
        { source: '입학', target: '사회과학대학', value: 80 },
        { source: '경영대학', target: '졸업', value: 70 },
        { source: '경영대학', target: '자연진급', value: 20 },
        { source: '경영대학', target: '학사경고', value: 8 },
        { source: '공과대학', target: '졸업', value: 100 },
        { source: '공과대학', target: '자연진급', value: 35 },
        { source: '공과대학', target: '학사경고', value: 12 },
        { source: '공과대학', target: '제적', value: 3 },
        { source: '사회과학대학', target: '졸업', value: 60 },
        { source: '사회과학대학', target: '자연진급', value: 15 },
        { source: '사회과학대학', target: '학사경고', value: 4 },
        { source: '학사경고', target: '제적', value: 5 }
      ]
    }]
  }
}

function TestChartPage() {
  const [selectedPreset, setSelectedPreset] = useState('bar')
  const [customConfig, setCustomConfig] = useState('')
  const [customConfigData, setCustomConfigData] = useState(null)
  const [error, setError] = useState(null)

  const currentConfig = customConfigData || presets[selectedPreset]

  const handleApplyCustom = () => {
    try {
      const parsed = JSON.parse(customConfig)
      setCustomConfigData(parsed)
      setError(null)
    } catch (e) {
      setError('유효하지 않은 JSON 형식입니다: ' + e.message)
    }
  }

  const handlePresetChange = (e) => {
    setSelectedPreset(e.target.value)
    setCustomConfigData(null)
    setError(null)
  }

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">ECharts Test Page</h1>
      
      <div className="mb-4 flex gap-4 items-center">
        <div>
          <label className="block text-sm font-medium mb-1">Preset 차트 선택:</label>
          <select
            value={selectedPreset}
            onChange={handlePresetChange}
            className="border rounded px-3 py-2 min-w-[200px]"
          >
            <option value="bar">Bar Chart</option>
            <option value="line">Line Chart</option>
            <option value="pie">Pie Chart</option>
            <option value="scatter">Scatter Chart</option>
            <option value="boxplot">Boxplot Chart</option>
            <option value="heatmap">Heatmap Chart</option>
            <option value="sankey">Sankey Chart</option>
          </select>
        </div>
      </div>

      <div className="mb-4">
        <label className="block text-sm font-medium mb-1">커스텀 Config JSON:</label>
        <textarea
          value={customConfig}
          onChange={(e) => setCustomConfig(e.target.value)}
          placeholder='{"series": [{"type": "bar", "data": [...]}]}'
          className="w-full h-32 border rounded px-3 py-2 font-mono text-sm"
        />
        <button
          onClick={handleApplyCustom}
          className="mt-2 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
        >
          Apply Custom Config
        </button>
        {error && (
          <p className="mt-2 text-red-500 text-sm">{error}</p>
        )}
      </div>

      <div className="border-t pt-4">
        <h2 className="text-lg font-medium mb-2">현재 Config:</h2>
        <pre className="bg-gray-100 p-2 rounded text-xs overflow-auto max-h-40 mb-4">
          {JSON.stringify(currentConfig, null, 2)}
        </pre>
        <GraphView config={currentConfig} />
      </div>
    </div>
  )
}

export default TestChartPage
