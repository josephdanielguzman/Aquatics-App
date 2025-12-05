import {useQueryClient} from "@tanstack/react-query";
import {useMutation} from "@tanstack/react-query";
import {createAssignment, replaceAssignment} from "../api/assignments.js";
import { queryKeys } from "../constants/queryKeys.jsx";
import { message } from "antd";

export const useCreateAssignment = () => {
    const queryClient = useQueryClient()

    return useMutation({
        mutationFn: createAssignment,
        onSuccess: () => {
            message.success("Assignments created successfully.")
            queryClient.invalidateQueries(queryKeys.GUARDS)
        },
        onError: (error) => {
            message.error(`Failed to create Assignment: ${error.message}`)
        }
    })
}

export const useReplaceAssignment = (options = {}) => {
    const queryClient = useQueryClient()

    return useMutation({
        mutationFn: replaceAssignment,
        onSuccess: () => {
            message.success("Assignments created successfully.")
            queryClient.invalidateQueries(queryKeys.GUARDS, queryKeys.ROTATIONS)

            if (options.onSuccess) {
                options.onSuccess(data, variables, context)
            }
        },
        onError: (error) => {
            message.error(`Failed to create Assignments: ${error.message}`)
        }
    })
}