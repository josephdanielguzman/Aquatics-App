import { api } from '/src/api/axios.js'

export const getRotations = async () => {
    const { data } = await api.get('/rotations/')
    return data
}

export const getAvailableSpots = async () => {
    const { data } = await api.get('/rotations/available_spots')
    return data
}

export const createRotation = async ({rotation_id, payload}) => {
    const { data } = await api.post(`/rotations/${rotation_id}/rotate`, payload)
    return data
}