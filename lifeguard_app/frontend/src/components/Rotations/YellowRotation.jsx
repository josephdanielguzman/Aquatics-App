import {Button, TimePicker} from "antd";
import {HistoryOutlined, ReloadOutlined} from "@ant-design/icons";

export default function YellowRotation() {
    const format = 'h:mm A'
    return (
        <div className={'rounded-md bg-white h-full shadow'}>
            <div className={'bg-amber-400 border-yellow-500 border-1 rounded-t-md text-white font-sans p-3 pb-2'}>
                <div className={'flex justify-between'}>
                    <p className={'text-white font-sans font-bold text-xl'}>Yellow</p>
                    <div className={'flex gap-0.5'}>
                        <TimePicker format={format} />
                        <Button variant={'outlined'} color={'orange'} icon={<ReloadOutlined />}>Rotate</Button>
                    </div>
                </div>
                <p><HistoryOutlined /> Last Rotated: 10:50</p>
            </div>
        </div>
    )
}