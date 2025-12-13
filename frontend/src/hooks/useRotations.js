import {useQuery} from "@tanstack/react-query";
import {getRotations, getAvailableSpots} from "/src/api/rotations.js";
import {queryKeys} from "/src/constants/queryKeys.jsx"

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