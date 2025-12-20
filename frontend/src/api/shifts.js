import { api } from '/src/api/axios.js'

export const createShift = async (payload) => {
    const { data } = await api.post('/shifts/', payload)
    return data
}

export const updateShift = async ({shift_id, payload}) => {
    const { data } = await api.post(`/shifts/${shift_id}/clock_out`, payload)
    return data
}