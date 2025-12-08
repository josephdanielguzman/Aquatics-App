import { api } from '/src/api/axios.js'

export const createBreak = async (payload) => {
    const { data } = await api.post('/breaks/', payload)
    return data
}

export const updateBreak = async ({id, payload}) => {
    const { data } = await api.patch(`/breaks/end_break/${id}`, payload)
    return data
}