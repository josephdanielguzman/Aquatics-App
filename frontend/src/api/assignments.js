import { api } from '/src/api/axios.js';

export const createAssignment = async (payload) => {
    const { data } = await api.post('/assignments/', payload)
    return data
}

export const replaceAssignment = async ({id, payload}) => {
    const { data } = await api.patch(`/assignments/replace/${id}`, payload)
    return data
}