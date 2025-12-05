import { api } from './axios.js'

export const getGuardsOnShift = async () => {
    const { data } = await api.get('/guards/on_shift')
    return data
}

export const getAvailableGuards = async () => {
    const { data } = await api.get('/guards/available')
    return data
}