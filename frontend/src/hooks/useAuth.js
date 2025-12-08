import {useMutation, useQueryClient} from "@tanstack/react-query";
import {login, verifyToken} from "../api/auth.js";
import {message} from "antd";
import { useNavigate } from "react-router-dom";

export const useLogin = () => {
    const navigate = useNavigate()

    return useMutation({
        mutationFn: login,
        onSuccess: (data) => {
            localStorage.setItem("token", data.access_token)
            message.success("Logged in successfully.")
            navigate('/')
        },
        onError: (error) => {
            message.error(`Error logging in.`)
        }
    })
}

export const useVerifyToken = () => {
    const navigate = useNavigate()

    return useMutation({
        mutationFn: verifyToken,
        onSuccess: () => {
            message.success("Valid token.")
            navigate('/')
        },
        onError: (error) => {
            message.error("Invalid token.")
            localStorage.removeItem("access_token")
            navigate('/login')
        }
    })
}