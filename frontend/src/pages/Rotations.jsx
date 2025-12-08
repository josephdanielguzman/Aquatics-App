import VioletRotation from '/src/components/Rotations/VioletRotation.jsx'
import GreenRotation from "/src/components/Rotations/GreenRotation.jsx";
import YellowRotation from "/src/components/Rotations/YellowRotation.jsx"
import {useRotations} from '/src/hooks/useRotations'
import {Skeleton} from "antd";

export default function Rotations() {
    const rotations = useRotations()

    if (rotations.isLoading) {
        return <Skeleton active paragraph={{rows: 4}}/>
    }

    const violet = rotations.data?.find(r => r.name === 'Violet')
    const yellow = rotations.data?.find(r => r.name === 'Yellow')
    const green = rotations.data?.find(r => r.name === 'Green')

    return(
        <div className={'h-auto flex flex-col mt-5'}>
            <VioletRotation data={violet}/>
            <YellowRotation data={yellow}/>
            <GreenRotation data={green}/>
        </div>
    )
}