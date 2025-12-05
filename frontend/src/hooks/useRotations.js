import {useQuery} from "@tanstack/react-query";
import {getRotations} from "../api/rotations.js";
import {queryKeys} from "../constants/queryKeys.jsx"

export const useRotations = () => {
    console.log("Use rotations...")
    return useQuery({
        queryKey: queryKeys.ROTATIONS,
        queryFn: getRotations,
        staleTime: 5 * 60 * 1000,
    })
}