import {Button, TimePicker} from "antd";
import {ReloadOutlined, HistoryOutlined, DownOutlined} from "@ant-design/icons";
import {useState} from "react";
import RotationData from "/src/components/RotationData.jsx"
import {useCreateRotation} from "/src/hooks/useRotations.js";
import {executeRotation} from "/src/utils/rotate.js";

export default function VioletRotation(props) {
    const format = 'h:mm A'

    // useStates
    const [showData, setShowData] = useState(false)
    const [time, setTime] = useState(null)
    const [timeRotated, setTimeRotated] = useState("N/A")

    // hooks
    const rotateMutation = useCreateRotation()

    // functions
    const handleRotate = () => {
        executeRotation(rotateMutation, 1, time)
        setTimeRotated(time)
    }

    const handleTimeChange = (timeValue, timeString) => {
        setTime(timeValue.format('HH:mm'))
    }

    const handleClick = () => {
        setShowData(!showData)
    }

    return (
        <div>
            <div className={'bg-pink-400 border-pink-500 border-1 rounded-t-md text-white font-sans p-3 pb-2'}>
                <div className={'flex gap-x-3'}>
                    <div className={'flex items-center pb-2'}>
                      <Button
                          onClick={handleClick}
                          variant={'outlined'}
                          color={'pink'}
                          icon={<DownOutlined/>}
                      />
                    </div>
                    <div className={'flex justify-between w-full'}>
                        <div>
                            <p className={'text-white font-sans font-bold text-xl'}>
                                Violet
                            </p>
                            <p>
                                <HistoryOutlined /> Last Rotated: {timeRotated}
                            </p>
                        </div>
                        <div className={'flex gap-0.5 h-min'}>
                            <TimePicker
                                format={format}
                                onChange={handleTimeChange}
                            />
                            <Button
                                onClick={handleRotate}
                                variant={'outlined'}
                                color={'pink'}
                                icon={<ReloadOutlined />}
                            >
                                Rotate
                            </Button>
                        </div>
                    </div>
                </div>
            </div>
            {showData && (
                <div className={'rounded-b-md bg-white h-auto p-4 shadow'}>
                    <RotationData data={props.data}/>
                </div>
            )}
        </div>
    )
}