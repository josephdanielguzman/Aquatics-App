import { api } from './axios.js'

export const getRotations = async () => {
    const { data } = await api.get('/rotations')
    return data
}