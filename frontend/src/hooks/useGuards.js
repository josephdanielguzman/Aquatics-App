import {getAvailableGuards, getGuardsOnShift} from "../api/guards.js";
import {useQuery} from "@tanstack/react-query";
import {queryKeys} from "../constants/queryKeys.jsx";

export const useGuardsOnShift = () => {
    console.log("Use guards on shift...")
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