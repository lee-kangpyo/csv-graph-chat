import api from './csvApi'

export const getBaskets = async () => {
  const response = await api.get('/api/basket/')
  return response.data
}

export const createBasket = async (name, graphConfig) => {
  const response = await api.post('/api/basket/', {
    name,
    graph_config: graphConfig,
  })
  return response.data
}

export const getBasket = async (id) => {
  const response = await api.get(`/api/basket/${id}`)
  return response.data
}

export const deleteBasket = async (id) => {
  const response = await api.delete(`/api/basket/${id}`)
  return response.data
}
