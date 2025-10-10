import {Button, TimePicker} from "antd";
import {ReloadOutlined, HistoryOutlined, DownOutlined} from "@ant-design/icons";
import {useState} from "react";

export default function VioletRotation() {
    const format = 'h:mm A'
    const [showData, setShowData] = useState(false)

    const handleClick = () => {
        setShowData(!showData)
    }

    return (
        <div>
            <div className={'bg-pink-400 border-pink-500 border-1 rounded-t-md text-white font-sans p-3 pb-2'}>
                <div className={'flex gap-x-3'}>
                    <div className={'flex items-center pb-2'}>
                      <Button onClick={handleClick} variant={'outlined'} color={'pink'} icon={<DownOutlined/>}></Button>
                    </div>
                    <div className={'flex justify-between w-full'}>
                        <div>
                            <p className={'text-white font-sans font-bold text-xl'}>Violet</p>
                            <p><HistoryOutlined /> Last Rotated: 10:50</p>
                        </div>
                        <div className={'flex gap-0.5 h-min'}>
                            <TimePicker format={format} />
                            <Button variant={'outlined'} color={'pink'} icon={<ReloadOutlined />}>Rotate</Button>
                        </div>
                    </div>
                </div>
            </div>
            {showData && (
                <div className={'rounded-b-md bg-white h-auto shadow'}>
                    <p>
                        print this
                    </p>
                </div>
            )}
        </div>
    )
}