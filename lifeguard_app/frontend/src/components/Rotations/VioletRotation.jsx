import {Button, TimePicker} from "antd";
import {ReloadOutlined, HistoryOutlined} from "@ant-design/icons";

export default function VioletRotation() {
    const format = 'h:mm A'
    return (
        <div className={'rounded-md bg-white h-full shadow'}>
            <div className={'bg-pink-400 border-pink-500 border-1 rounded-t-md text-white font-sans p-3 pb-2'}>
                <div className={'flex justify-between'}>
                    <p className={'text-white font-sans font-bold text-xl'}>Violet</p>
                    <div className={'flex gap-0.5'}>
                        <TimePicker format={format} />
                        <Button variant={'outlined'} color={'pink'} icon={<ReloadOutlined />}>Rotate</Button>
                    </div>
                </div>
                <p><HistoryOutlined /> Last Rotated: 10:50</p>
            </div>
        </div>
    )
}