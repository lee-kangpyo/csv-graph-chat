import { useState } from 'react'
import ChatArea from './components/ChatArea'
import ChatInput from './components/ChatInput'
import BasketSidebar from './components/BasketSidebar'
import GraphModal from './components/GraphModal'
import Toast from './components/Toast'
import TestChartPage from './components/TestChartPage'
import './App.css'

function App() {
  const [toast, setToast] = useState(null)
  const [selectedGraph, setSelectedGraph] = useState(null)
  const [isModalOpen, setIsModalOpen] = useState(false)

  const isTestMode = new URLSearchParams(window.location.search).get('test') === '1'

  const showToast = (message, type = 'error') => {
    setToast({ message, type })
    setTimeout(() => setToast(null), 3000)
  }

  const openGraphModal = (graph) => {
    setSelectedGraph(graph)
    setIsModalOpen(true)
  }

  const closeGraphModal = () => {
    setIsModalOpen(false)
    setSelectedGraph(null)
  }

  if (isTestMode) {
    return (
      <div className="min-h-screen bg-white">
        <TestChartPage />
      </div>
    )
  }

  return (
    <div className="app-container flex h-screen">
      <BasketSidebar onShowToast={showToast} onGraphClick={openGraphModal} />

      <main className="flex-1 flex flex-col">
        <ChatArea onShowToast={showToast} />
        <ChatInput onShowToast={showToast} />
      </main>

      <GraphModal
        isOpen={isModalOpen}
        onClose={closeGraphModal}
        graphConfig={selectedGraph?.graph_config}
        userQuestion={selectedGraph?.question}
      />

      {toast && <Toast message={toast.message} type={toast.type} />}
    </div>
  )
}

export default App
