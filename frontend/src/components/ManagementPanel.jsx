import {EnvironmentOutlined, UserOutlined} from "@ant-design/icons";
import BreakEdit from "/src/components/ManagementPanel/BreakEdit.jsx";


export default function ManagementPanel(props) {

    const noSpot = props.guard.rotation === null
    const finalBreak = props.guard.breaks?.[2]
    const breakAvailable = !finalBreak || finalBreak.ended === null

    return (
        <div className={'bg-white h-auto rounded-md shadow font-semibold'}>
            <div className={'p-3 border-b-1 border-gray-200'}>
                <p className={'text-xl text-neutral-800'}>Management Panel</p>
            </div>
            <div className={'flex flex-col gap-y-10 p-4'}>
                <div className={' flex flex-col gap-y-2 rounded-md bg-blue-100 p-4 text-blue-900 font-normal'}>
                    <p className={'text-lg font-semibold'}>Selected Lifeguard:</p>
                    <div>
                        <p><UserOutlined /> {props.guard.name}</p>
                        <p className={'pt-1'}><EnvironmentOutlined/> {props.guard.spot_name ? props.guard.spot_name : 'N/A'}</p>
                    </div>
                </div>
                {(breakAvailable && noSpot) && <BreakEdit guard={props.guard}/>}
                <SpotEdit guard={props.guard}/>

            </div>
        </div>
    )
}