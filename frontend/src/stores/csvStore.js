import { create } from 'zustand'

const useCSVStore = create((set) => ({
  fileId: null,
  fileName: null,
  columns: [],
  rowCount: 0,
  
  setCSVData: (data) => set({
    fileId: data.file_id,
    fileName: data.filename,
    rowCount: data.row_count,
    columns: data.columns || []
  }),
  
  updateColumnName: (originalName, newName) => set((state) => ({
    columns: state.columns.map(col => 
      col.name === originalName 
        ? { ...col, inferred_name: newName }
        : col
    )
  })),
  
  clearCSV: () => set({
    fileId: null,
    fileName: null,
    columns: [],
    rowCount: 0
  }),
}))

export default useCSVStore
