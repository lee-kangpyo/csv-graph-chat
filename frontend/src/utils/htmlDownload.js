export const generateGraphsHTML = (graphs) => {
  const chartsHTML = graphs.map((graph, idx) => `
    <div class="chart-container" style="margin-bottom: 40px; border: 1px solid #ddd; padding: 20px; border-radius: 8px;">
      <h3 style="margin-top: 0;">${escapeHTML(graph.name)}</h3>
      <canvas id="chart${idx}"></canvas>
    </div>
  `).join('')

  const chartScripts = graphs.map((graph, idx) => `
    new Chart(document.getElementById('chart${idx}'), ${JSON.stringify(graph.graph_config)});
  `).join('\n')

  return `<!DOCTYPE html>
<html>
<head>
  <title>CSV Graph Chat - Graphs</title>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <style>
    body { font-family: system-ui, -apple-system, sans-serif; padding: 20px; max-width: 1200px; margin: 0 auto; }
    h1 { color: #333; }
    .chart-container { margin-bottom: 40px; border: 1px solid #ddd; padding: 20px; border-radius: 8px; }
    h3 { margin-top: 0; color: #555; }
  </style>
</head>
<body>
  <h1>My Graphs</h1>
  <p>Generated on ${new Date().toLocaleDateString()}</p>
  ${chartsHTML}
  <script>
    ${chartScripts}
  </script>
</body>
</html>`
}

export const downloadHTML = (graphs, filename = 'graphs.html') => {
  const html = generateGraphsHTML(graphs)
  const blob = new Blob([html], { type: 'text/html' })
  const url = URL.createObjectURL(blob)
  
  const a = document.createElement('a')
  a.href = url
  a.download = filename
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
}

const escapeHTML = (str) => {
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;')
}
