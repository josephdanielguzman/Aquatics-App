import {useQuery} from "@tanstack/react-query";
import {getRotations} from "/src/api/rotations.js";
import {queryKeys} from "/src/constants/queryKeys.jsx"

export const useRotations = () => {
    return useQuery({
        queryKey: queryKeys.ROTATIONS,
        queryFn: getRotations,
        staleTime: 5 * 60 * 1000,
    })
}