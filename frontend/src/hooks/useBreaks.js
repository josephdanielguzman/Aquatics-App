import {createBreak, updateBreak} from '../api/breaks.js'
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { queryKeys } from '../constants/queryKeys.jsx'
import { message } from 'antd'

export const useCreateBreak = () => {
    const queryClient = useQueryClient()

    return useMutation({
        mutationFn: createBreak,
        onSuccess: () => {
            queryClient.invalidateQueries(queryKeys.GUARDS.ON_SHIFT)
            message.success("Break modified successfully.")
        },
        onError: (error) => {
            message.error(`Error modifying break: ${error.message}`)
        }
    })
}

export const useUpdateBreak = () => {
    const queryClient = useQueryClient()

    return useMutation({
        mutationFn: updateBreak,
        onSuccess: () => {
            queryClient.invalidateQueries(queryKeys.GUARDS.ON_SHIFT)
            message.success("Break modified successfully.")
        },
        onError: (error) => {
            message.error(`Error modifying break: ${error.message}`)
        }
    })
}