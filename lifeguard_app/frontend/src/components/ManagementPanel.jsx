import { UserOutlined } from "@ant-design/icons";
import BreakEdit from "./ManagementPanel/BreakEdit.jsx";
import SpotEdit from "./ManagementPanel/SpotEdit.jsx";


export default function ManagementPanel(props) {
    const format = 'h:mm A'
    return (
        <div className={'bg-white h-auto rounded-md shadow font-bold'}>
            <div className={'p-4 border-b-1 border-gray-200'}>
                <p className={'text-xl text-neutral-800'}>Management Panel</p>
            </div>
            <div className={'flex flex-col gap-y-10 p-4'}>
                <div className={' flex flex-col gap-y-2 rounded-md bg-blue-100 p-4 text-blue-900 font-normal'}>
                    <p className={'text-lg font-semibold'}>Selected Lifeguard:</p>
                    <div>
                        <p><UserOutlined /> {props.guard.name}</p>
                        <p className={'pt-1'}> {props.guard.spot_name}</p>
                    </div>
                </div>
                <BreakEdit guard={props}/>
                <SpotEdit guard={props}/>
            </div>
        </div>
    )
}