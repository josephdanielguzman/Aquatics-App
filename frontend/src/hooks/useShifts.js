import { useMutation, useQueryClient } from "@tanstack/react-query";
import {createShift} from "../api/shifts.js";
import { message } from 'antd';
import { queryKeys} from "../constants/queryKeys.jsx";

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