import VioletRotation from '../components/Rotations/VioletRotation.jsx'
import GreenRotation from "../components/Rotations/GreenRotation.jsx";
import YellowRotation from "../components/Rotations/YellowRotation.jsx"

export default function Rotations() {
    return(
        <div className={'h-screen flex flex-col justify-between mt-5 space-y-7'}>
            <VioletRotation/>
            <YellowRotation/>
            <GreenRotation/>
        </div>
    )
}