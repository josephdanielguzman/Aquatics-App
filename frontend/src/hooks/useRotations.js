import {useMutation, useQuery, useQueryClient} from "@tanstack/react-query";
import {getRotations, getAvailableSpots, createRotation, getRotationTime} from "/src/api/rotations.js";
import {queryKeys} from "/src/constants/queryKeys.jsx"
import {message} from "antd";

export const useRotations = () => {
    return useQuery({
        queryKey: queryKeys.ROTATIONS.ALL,
        queryFn: getRotations,
        staleTime: 5 * 60 * 1000
    })
}

export const useAvailableSpots = () => {
    return useQuery({
        queryKey: queryKeys.ROTATIONS.AVAIL_SPOTS,
        queryFn: getAvailableSpots,
        staleTime: 5 * 60 * 1000
        })
}

export const useCreateRotation = () => {
    const queryClient = useQueryClient()

    return useMutation({
        mutationFn: createRotation,
        onSuccess: () => {
            queryClient.invalidateQueries(queryKeys.ROTATIONS.ALL)
            message.success("All guards rotated")
        },
        onError: (error) => {
            message.error(`Unable to rotate guards: ${error.message}`)
        }
    })
}

export const useRotationTime = (rotation_id) => {
    return useQuery({
        queryKey: [...queryKeys.ROTATIONS.LAST_ROTATED, rotation_id],
        queryFn: () => getRotationTime({rotation_id}),
        staleTime: 5 * 60 * 1000,
        enabled: !!rotation_id
    })
}