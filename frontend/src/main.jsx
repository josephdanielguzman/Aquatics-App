import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { createBrowserRouter, RouterProvider } from "react-router-dom"
import { QueryClient, QueryClientProvider } from "@tanstack/react-query"
import Dashboard from '/src/pages/Dashboard.jsx'
import Rotations from '/src/pages/Rotations.jsx'
import Reports from "/src/pages/Reports.jsx"
import Login from "/src/components/Login.jsx"
import '/src/index.css'
import Protected from "/src/components/Protected.jsx";

const queryClient = new QueryClient()

const router = createBrowserRouter([
    {
        path: '/login',
        element: <Login />
    },
    {
        path: '/',
        element: <Protected />,
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
