import { api } from '/src/api/axios.js'

export const getRotations = async () => {
    const { data } = await api.get('/rotations')
    return data
}