import {getAvailableGuards, getGuardsOnShift, getGuardsOnShiftNoSpot} from "/src/api/guards.js";
import {useQuery} from "@tanstack/react-query";
import {queryKeys} from "/src/constants/queryKeys.jsx";

export const useGuardsOnShift = () => {
    return useQuery({
        queryKey: queryKeys.GUARDS.ON_SHIFT,
        queryFn: getGuardsOnShift,
        staleTime: 5 * 60 * 1000
    })
}

export const useAvailableGuards = () => {
    return useQuery({
        queryKey: queryKeys.GUARDS.AVAILABLE,
        queryFn: getAvailableGuards,
        staleTime: 5 * 60 * 1000
    })
}

export const useGetGuardsOnShiftNoSpot = () => {
    return useQuery({
        queryKey: queryKeys.GUARDS.ON_SHIFT_NO_SPOT,
        queryFn: getGuardsOnShiftNoSpot,
        staleTime: 5 * 60 * 1000
    })
}