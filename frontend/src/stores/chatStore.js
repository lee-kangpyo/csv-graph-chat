import { create } from 'zustand'

const useChatStore = create((set) => ({
  messages: [],
  isLoading: false,
  
  addMessage: (role, content, suggestions = []) => set((state) => ({
    messages: [...state.messages, { role, content, timestamp: Date.now(), suggestions }]
  })),
  
  clearMessages: () => set({ messages: [] }),
  
  setMessages: (messages) => set({ messages }),
  
  setLoading: (loading) => set({ isLoading: loading }),
}))

export default useChatStore
