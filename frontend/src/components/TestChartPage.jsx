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
  },
  radar: {
    title: { text: 'Radar Chart - 학생 역량 평가' },
    tooltip: {},
    radar: {
      indicator: [
        { name: '학점', max: 4.5 },
        { name: '출석', max: 100 },
        { name: '과제', max: 100 },
        { name: '중간고사', max: 100 },
        { name: '기말고사', max: 100 },
        { name: '프로젝트', max: 100 }
      ],
      center: ['50%', '55%']
    },
    series: [{
      type: 'radar',
      data: [
        {
          value: [3.8, 95, 85, 78, 92, 88],
          name: '학생 A'
        },
        {
          value: [3.5, 88, 90, 85, 80, 75],
          name: '학생 B'
        }
      ]
    }]
  },
  polar: {
    title: { text: 'Polar Chart - 학기별 활동량' },
    tooltip: { trigger: 'item' },
    angleAxis: {
      type: 'category',
      data: ['독서', '팀플', '발표', '시험', '과제', '자습']
    },
    radiusAxis: {},
    polar: {},
    series: [{
      type: 'bar',
      data: [45, 60, 35, 80, 55, 40],
      coordinateSystem: 'polar',
      name: '활동량',
      stack: 'a'
    }, {
      type: 'bar',
      data: [20, 35, 45, 30, 25, 30],
      coordinateSystem: 'polar',
      name: '참여도',
      stack: 'a'
    }]
  },
  graph: {
    title: { text: 'Graph Chart - 친구 관계도' },
    tooltip: { trigger: 'item' },
    series: [{
      type: 'graph',
      layout: 'force',
      symbolSize: 40,
      roam: true,
      label: { show: true, position: 'bottom' },
      edgeSymbol: ['circle', 'arrow'],
      edgeSymbolSize: [4, 10],
      data: [
        { name: '김同学', symbolSize: 60 },
        { name: '이同学', symbolSize: 50 },
        { name: '박同学', symbolSize: 45 },
        { name: '정同学', symbolSize: 40 },
        { name: '최同学', symbolSize: 35 },
        { name: '강同学', symbolSize: 35 }
      ],
      links: [
        { source: '김同学', target: '이同学', lineStyle: { width: 3 } },
        { source: '김同学', target: '박同学', lineStyle: { width: 2 } },
        { source: '이同学', target: '정同学', lineStyle: { width: 4 } },
        { source: '박同学', target: '최同学', lineStyle: { width: 2 } },
        { source: '정同学', target: '최同学', lineStyle: { width: 3 } },
        { source: '최同学', target: '강同学', lineStyle: { width: 2 } }
      ],
      lineStyle: { opacity: 0.6, curveness: 0.2 }
    }]
  },
  tree: {
    title: { text: 'Tree Chart - 학과 구조' },
    tooltip: { trigger: 'item' },
    series: [{
      type: 'tree',
      data: [
        {
          name: '총장',
          children: [
            {
              name: '교학처',
              children: [
                { name: '입시팀' },
                { name: '교육팀' }
              ]
            },
            {
              name: '학생처',
              children: [
                { name: '학생지원팀' },
                { name: '취업팀' }
              ]
            },
            {
              name: '기획처',
              children: [
                { name: '예산팀' },
                { name: '시설팀' }
              ]
            }
          ]
        }
      ],
      label: { position: 'left', verticalAlign: 'middle', align: 'right' },
      orient: 'LR'
    }]
  },
  sunburst: {
    title: { text: 'Sunburst Chart - 학점 분포' },
    tooltip: { trigger: 'item' },
    series: [{
      type: 'sunburst',
      data: [
        {
          name: '졸업요건',
          children: [
            {
              name: '전공',
              value: 60,
              children: [
                { name: '필수', value: 35 },
                { name: '선택', value: 25 }
              ]
            },
            {
              name: '교양',
              value: 30,
              children: [
                { name: '핵심', value: 15 },
                { name: '일반', value: 15 }
              ]
            },
            {
              name: '일반선택',
              value: 10
            }
          ]
        }
      ],
      radius: ['15%', '80%'],
      label: { rotate: 'radial' }
    }]
  },
  treemap: {
    title: { text: 'Treemap - 강의 평가 항목' },
    tooltip: { trigger: 'item' },
    series: [{
      type: 'treemap',
      data: [
        {
          name: '강의평가',
          children: [
            { name: '수업내용', value: 30 },
            { name: '교수법', value: 25 },
            { name: '성적기준', value: 20 },
            { name: '자료제공', value: 15 },
            { name: '答疑态度', value: 10 }
          ]
        }
      ]
    }]
  },
  parallel: {
    title: { text: 'Parallel Chart - 학생 프로파일' },
    tooltip: { trigger: 'item' },
    parallelAxis: [
      { dim: 0, name: '학점' },
      { dim: 1, name: '출석률' },
      { dim: 2, name: '과제점수' },
      { dim: 3, name: '중간고사' },
      { dim: 4, name: '기말고사' }
    ],
    series: [{
      type: 'parallel',
      data: [
        [3.8, 95, 85, 78, 92],
        [3.5, 88, 90, 85, 80],
        [4.0, 100, 95, 90, 95],
        [3.2, 75, 80, 70, 75],
        [3.6, 90, 88, 82, 88]
      ]
    }]
  },
  gauge: {
    title: { text: 'Gauge Chart - 학업 달성도' },
    tooltip: { formatter: '{a} <br/>{b} : {c}%' },
    series: [{
      type: 'gauge',
      detail: { formatter: '{value}%' },
      data: [{ value: 78, name: '달성도' }],
      min: 0,
      max: 100
    }]
  },
  funnel: {
    title: { text: 'Funnel Chart - 입학->졸업 funnel' },
    tooltip: { trigger: 'item' },
    series: [{
      type: 'funnel',
      left: '10%',
      top: 60,
      bottom: 60,
      width: '80%',
      min: 0,
      max: 100,
      minSize: '0%',
      maxSize: '100%',
      gap: 2,
      label: { show: true, position: 'inside' },
      data: [
        { value: 100, name: '입학' },
        { value: 80, name: '2학년 진급' },
        { value: 60, name: '3학년 진급' },
        { value: 40, name: '4학년 진급' },
        { value: 20, name: '졸업' }
      ]
    }]
  },
  candlestick: {
    title: { text: 'Candlestick Chart - 주간 주가' },
    tooltip: { trigger: 'item' },
    xAxis: {
      type: 'category',
      data: ['周一', '周二', '周三', '周四', '周五']
    },
    yAxis: { type: 'value', scale: true },
    series: [{
      type: 'candlestick',
      data: [
        [20, 30, 10, 35],
        [32, 35, 28, 38],
        [30, 38, 25, 40],
        [35, 42, 30, 45],
        [40, 48, 35, 50]
      ]
    }]
  },
  
  calendar: {
    title: { text: 'Calendar Chart - 학습 시간 히트맵' },
    tooltip: { trigger: 'item' },
    visualMap: {
      min: 0,
      max: 10,
      calculable: true,
      orient: 'vertical',
      left: 'right',
      top: 'center'
    },
    calendar: {
      range: '2024-01'
    },
    series: [{
      type: 'heatmap',
      coordinateSystem: 'calendar',
      data: [
        ['2024-01-01', 5],
        ['2024-01-02', 3],
        ['2024-01-03', 7],
        ['2024-01-04', 2],
        ['2024-01-05', 8],
        ['2024-01-06', 6],
        ['2024-01-07', 4],
        ['2024-01-08', 5],
        ['2024-01-09', 3],
        ['2024-01-10', 6],
        ['2024-01-11', 7],
        ['2024-01-12', 4],
        ['2024-01-13', 2],
        ['2024-01-14', 8],
        ['2024-01-15', 5],
        ['2024-01-16', 3],
        ['2024-01-17', 6],
        ['2024-01-18', 7],
        ['2024-01-19', 4],
        ['2024-01-20', 2],
        ['2024-01-21', 9],
        ['2024-01-22', 5],
        ['2024-01-23', 3],
        ['2024-01-24', 6],
        ['2024-01-25', 7],
        ['2024-01-26', 4],
        ['2024-01-27', 2],
        ['2024-01-28', 8],
        ['2024-01-29', 5],
        ['2024-01-30', 3],
        ['2024-01-31', 6]
      ]
    }]
  }
}

function TestChartPage() {
  const [selectedPreset, setSelectedPreset] = useState('bar')
  const [customConfig, setCustomConfig] = useState('')
  const [customConfigData, setCustomConfigData] = useState(null)
  const [error, setError] = useState(null)
  const [configCollapsed, setConfigCollapsed] = useState(true)
  const [currentConfigCollapsed, setCurrentConfigCollapsed] = useState(true)

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
            <option value="radar">Radar Chart</option>
            <option value="polar">Polar Chart</option>
            <option value="graph">Graph Chart</option>
            <option value="tree">Tree Chart</option>
            <option value="sunburst">Sunburst Chart</option>
            <option value="treemap">Treemap Chart</option>
            <option value="parallel">Parallel Chart</option>
            <option value="gauge">Gauge Chart</option>
            <option value="funnel">Funnel Chart</option>
            <option value="candlestick">Candlestick Chart</option>
            <option value="themeriver">ThemeRiver Chart</option>
            <option value="calendar">Calendar Chart</option>
          </select>
        </div>
      </div>

      <div className="mb-4">
        <button
          onClick={() => setConfigCollapsed(!configCollapsed)}
          className="flex items-center gap-2 text-sm font-medium mb-2"
        >
          <span className="text-xs">{configCollapsed ? '▶' : '▼'}</span>
          커스텀 Config JSON {configCollapsed ? '(접힘)' : '(펼침)'}
        </button>
        
        {!configCollapsed && (
          <>
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
          </>
        )}
      </div>

      <div className="border-t pt-4">
        <button
          onClick={() => setCurrentConfigCollapsed(!currentConfigCollapsed)}
          className="flex items-center gap-2 text-sm font-medium mb-2"
        >
          <span className="text-xs">{currentConfigCollapsed ? '▶' : '▼'}</span>
          현재 Config {currentConfigCollapsed ? '(접힘)' : '(펼침)'}
        </button>
        
        {!currentConfigCollapsed && (
          <pre className="bg-gray-100 p-2 rounded text-xs overflow-auto max-h-40 mb-4">
            {JSON.stringify(currentConfig, null, 2)}
          </pre>
        )}
        <GraphView config={currentConfig} />
      </div>
    </div>
  )
}

export default TestChartPage