import { create } from 'zustand'

const useGraphStore = create((set) => ({
  currentGraph: null,
  isLoading: false,
  
  setCurrentGraph: (graph) => set({ currentGraph: graph }),
  
  setLoading: (loading) => set({ isLoading: loading }),
  
  clearGraph: () => set({ currentGraph: null }),
}))

export default useGraphStore
