import { useVerifyToken } from "../hooks/useAuth.js";
import {useNavigate} from "react-router-dom";
import {useEffect} from "react";
import MainLayout from "../layout/MainLayout.jsx";

export default function Protected() {

    const verifyToken = useVerifyToken()
    const navigate = useNavigate()

    useEffect(() => {
        verifyToken.mutate()
    }, [navigate])

    return (
        <MainLayout/>
    )
}