import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { createBrowserRouter, RouterProvider } from "react-router-dom"
import { QueryClient, QueryClientProvider } from "@tanstack/react-query"
import MainLayout from './layout/MainLayout.jsx'
import Dashboard from './pages/Dashboard.jsx'
import Rotations from './pages/Rotations.jsx'
import Reports from "./pages/Reports.jsx"
import './index.css'

const queryClient = new QueryClient()

const router = createBrowserRouter([
    {
        path: '/',
        element: <MainLayout />,
        children: [
            {index: true, element: <Dashboard />},
            {path: '/Rotations', element: <Rotations />},
            {path: '/Reports', element: <Reports />},
        ]
    }
])

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <QueryClientProvider client={queryClient}>
        <RouterProvider router = {router} />
    </QueryClientProvider>
  </StrictMode>,
)
