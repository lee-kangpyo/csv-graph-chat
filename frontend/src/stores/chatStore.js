import { create } from 'zustand'

const useChatStore = create((set) => ({
  messages: [],
  isLoading: false,
  
  addMessage: (role, content) => set((state) => ({
    messages: [...state.messages, { role, content, timestamp: Date.now() }]
  })),
  
  clearMessages: () => set({ messages: [] }),
  
  setMessages: (messages) => set({ messages }),
  
  setLoading: (loading) => set({ isLoading: loading }),
}))

export default useChatStore
