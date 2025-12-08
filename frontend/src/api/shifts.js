import { api } from '/src/api/axios.js'

export const createShift = async (payload) => {
    const { data } = await api.post('/shifts/', payload)
    return data
}