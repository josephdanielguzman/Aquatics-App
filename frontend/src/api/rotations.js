import { api } from '/src/api/axios.js'

export const getRotations = async () => {
    const { data } = await api.get('/rotations')
    return data
}

export const getAvailableSpots = async () => {
    const { data } = await api.get('/rotations/available_spots')
    return data
}
