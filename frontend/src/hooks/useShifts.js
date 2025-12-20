import { useMutation, useQueryClient } from "@tanstack/react-query";
import {createShift, updateShift} from "/src/api/shifts.js";
import { message } from 'antd';
import { queryKeys} from "/src/constants/queryKeys.jsx";

export const useCreateShift = (options = {}) => {
    const queryClient = useQueryClient()

    return useMutation({
        mutationFn: createShift,
        onSuccess: (data, variables, context) => {
            message.success('Shift created successfully.')
            queryClient.invalidateQueries(queryKeys.GUARDS)

            if (options.onSuccess) {
                options.onSuccess(data, variables, context)
            }
        },
        onError: (error) => {
            message.error(`Failed to create shift: ${error.message}`)
        }
    })
}

export const useUpdateShift = (options = {}) => {
    const queryClient = useQueryClient()

    return useMutation({
        mutationFn: updateShift,
        onSuccess: (data, variables, context) => {
            queryClient.invalidateQueries(queryKeys.GUARDS.ALL)
            message.success('Guard clocked out successfully.')

            if (options.onSuccess()) {
                options.onSuccess(data, variables, context)
            }
        },
        onError: (error) => {
            message.error(`Failed to clock out guard: ${error.message}`)
        }
    })
}