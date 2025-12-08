import { useVerifyToken } from "/src/hooks/useAuth.js";
import {useNavigate} from "react-router-dom";
import {useEffect} from "react";
import MainLayout from "/src/layout/MainLayout.jsx";

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