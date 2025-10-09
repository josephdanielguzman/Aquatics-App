import {Button, TimePicker} from "antd";
import {HistoryOutlined, ReloadOutlined} from "@ant-design/icons";

export default function GreenRotation() {
    const format = 'h:mm A'
    return(
        <div className={'rounded-md bg-white h-full shadow'}>
            <div className={'bg-green-500 border-green-600 border-1 rounded-t-md text-white font-sans p-3 pb-2'}>
                <div className={'flex justify-between'}>
                    <p className={'text-white font-sans font-bold text-xl'}>Green</p>
                    <div className={'flex gap-0.5'}>
                        <TimePicker format={format} />
                        <Button variant={'outlined'} color={'green'} icon={<ReloadOutlined />}>Rotate</Button>
                    </div>
                </div>
                <p><HistoryOutlined /> Last Rotated: 10:50</p>
            </div>
        </div>
    )
}