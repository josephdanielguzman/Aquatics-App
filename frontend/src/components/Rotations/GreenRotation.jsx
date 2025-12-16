import {Button, TimePicker} from "antd";
import {DownOutlined, HistoryOutlined, ReloadOutlined} from "@ant-design/icons";
import { useState } from "react";
import RotationData from "/src/components/RotationData.jsx";
import {useCreateRotation, useRotationTime} from "/src/hooks/useRotations.js";
import {executeRotation} from "/src/utils/rotate.js";
import {formatTime} from "/src/utils/formatTime.js";

export default function GreenRotation(props) {
    const format = 'h:mm A'

    // useStates
    const [showData, setShowData] = useState(false);
    const [time, setTime] = useState(null)

    // hooks
    const rotateMutation = useCreateRotation()
    const lastRotated = useRotationTime(2)

    // functions
    const handleRotate = () => {
        executeRotation(rotateMutation, 2, time)
    }

    const handleTimeChange = (timeValue, timeString) => {
        setTime(timeValue.format('HH:mm'))
    }

    const handleClick = () => {
        setShowData(!showData);
    }

    return(
        <div className={'mt-7 min-w-fit'}>
            <div className={'bg-green-500 border-green-600 border-1 rounded-t-md text-white font-sans p-3 pb-2'}>
                <div className={'flex gap-x-3'}>
                    <div className={'flex items-center pb-2'}>
                      <Button
                          onClick={handleClick}
                          variant={'outlined'}
                          color={'green'}
                          icon={<DownOutlined/>}
                      />
                    </div>
                    <div className={'flex justify-between w-full'}>
                        <div>
                            <p className={'text-white font-sans font-bold text-xl'}>
                                Green
                            </p>
                            <p>
                                <HistoryOutlined /> Last Rotated: {formatTime(lastRotated.data)}
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
                                color={'green'}
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