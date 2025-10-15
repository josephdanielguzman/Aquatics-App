import { api } from './axios.js'

export const getGuardsRoster = async () => {
    const { data } = await api.get('/guards')
    return data
}

export const getGuardsStatus = async () => {
    const { data } = await api.get('/guards/status');
    return data
}