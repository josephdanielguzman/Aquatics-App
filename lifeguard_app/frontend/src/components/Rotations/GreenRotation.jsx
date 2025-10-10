import {Button, TimePicker} from "antd";
import {DownOutlined, HistoryOutlined, ReloadOutlined} from "@ant-design/icons";
import { useState } from "react";

export default function GreenRotation() {
    const format = 'h:mm A'
    const [showData, setShowData] = useState(false);

    const handleClick = () => {
        setShowData(!showData);
    }
    return(
        <div className={'mt-7 min-w-fit'}>
            <div className={'bg-green-500 border-green-600 border-1 rounded-t-md text-white font-sans p-3 pb-2'}>
                <div className={'flex gap-x-3'}>
                    <div className={'flex items-center pb-2'}>
                      <Button onClick={handleClick} variant={'outlined'} color={'green'} icon={<DownOutlined/>}></Button>
                    </div>
                    <div className={'flex justify-between w-full'}>
                        <div>
                            <p className={'text-white font-sans font-bold text-xl'}>Green</p>
                            <p><HistoryOutlined /> Last Rotated: 10:50</p>
                        </div>
                        <div className={'flex gap-0.5 h-min'}>
                            <TimePicker format={format} />
                            <Button variant={'outlined'} color={'green'} icon={<ReloadOutlined />}>Rotate</Button>
                        </div>
                    </div>
                </div>
            </div>
            {showData && (
                <div className={'rounded-b-md bg-white h-full shadow'}>
                    <p>
                        print this
                    </p>
                </div>
            )}
        </div>
    )
}