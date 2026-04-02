import { create } from 'zustand'

const useBasketStore = create((set) => ({
  items: [],
  loading: false,
  
  setItems: (items) => set({ items }),
  
  addItem: (item) => set((state) => ({
    items: [...state.items, item]
  })),
  
  removeItem: (id) => set((state) => ({
    items: state.items.filter(item => item.id !== id)
  })),
  
  setLoading: (loading) => set({ loading }),
}))

export default useBasketStore
