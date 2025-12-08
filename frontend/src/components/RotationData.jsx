import {Steps} from "antd"
import {UserOutlined} from "@ant-design/icons";

export default function RotationData(props) {

    const spotsData = props.data.spots.map(spot => ({
        title: spot.name,
        description: spot.current_guard,
    }))

    const spotsItems = spotsData.map(spot => ({
        title: <p className={'font-bold !text-neutral-800'}>{spot.title}</p>,
        description: <p className={'!text-blue-900'}><UserOutlined /> {spot.description !== '' ? spot.description : 'N/A'}</p>
    }))

    return (
        <Steps items={spotsItems} direction={'vertical'}/>
    )
}