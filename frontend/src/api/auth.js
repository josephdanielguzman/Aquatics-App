import { api } from '/src/api/axios.js'

export const login = async(payload) => {
    const formData = new URLSearchParams()
    formData.append('username', payload.username)
    formData.append('password', payload.password)

    const { data } = await api.post("/auth/login", formData, {
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    })

    return data
}

export const verifyToken = async() => {
    const { data } = await api.post("/auth/verify-token")
    return data
}