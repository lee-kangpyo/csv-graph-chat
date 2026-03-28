import { useState } from 'react'
import ChatArea from './components/ChatArea'
import ChatInput from './components/ChatInput'
import BasketSidebar from './components/BasketSidebar'
import GraphView from './components/GraphView'
import Toast from './components/Toast'
import './App.css'

function App() {
  const [currentGraph, setCurrentGraph] = useState(null)
  const [toast, setToast] = useState(null)

  const showToast = (message, type = 'error') => {
    setToast({ message, type })
    setTimeout(() => setToast(null), 3000)
  }

  return (
    <div className="app-container flex h-screen">
      <BasketSidebar onShowToast={showToast} />
      
      <main className="flex-1 flex flex-col">
        <ChatArea 
          currentGraph={currentGraph} 
          onGraphGenerated={setCurrentGraph}
          onShowToast={showToast}
        />
        
        {currentGraph && (
          <div className="border-t border-gray-200 dark:border-gray-700">
            <GraphView config={currentGraph} />
          </div>
        )}
        
        <ChatInput 
          onShowToast={showToast}
          onGraphGenerated={setCurrentGraph}
        />
      </main>

      {toast && <Toast message={toast.message} type={toast.type} />}
    </div>
  )
}

export default App
