import { api } from '/src/api/axios.js'

export const getGuardsOnShift = async ({ guardId }) => {
    const { data } = await api.get('/guards/on_shift', {
        params: guardId ? { guard_id: guardId } : undefined
    })
    return data
}

export const getAvailableGuards = async () => {
    const { data } = await api.get('/guards/available')
    return data
}

export const getGuardsOnShiftNoSpot = async () => {
    const { data } = await api.get("/guards/on_shift/no_spot")
    return data
}