import { Table, Button, Tag } from 'antd';
import {useQuery} from "@tanstack/react-query";
import {
    CheckOutlined,
    ClockCircleOutlined,
    CloseOutlined,
} from "@ant-design/icons";
import {useState} from "react";


export default function GuardsTable(props){

    const [selectedId, setSelectedId] = useState(null);

    const handleClick = (recordId) => {
        if(recordId === selectedId){
            setSelectedId(null);
            props.onGuardSelect(false);
        } else {
            setSelectedId(recordId);
            props.onGuardSelect(true);
            props.setSelectedGuardId(recordId);

        }
    }

    const columns = [
        {
            title: 'Name',
            dataIndex: 'name',
            key: 'name',
        },
        {
            title: 'Clock-In',
            dataIndex: 'clock_in',
            key: 'clock_in',
            width: 150,
            render: (text, record) =>
                <p>{text}</p>

        },
        {
            title: 'Spot',
            dataIndex: 'spot_name',
            key: 'spot_name',
            render: (text, record) =>
                <Tag style={{fontSize: '14px'}}
                     color={(() => {
                    if (record.rotation === 'Violet') {
                        return 'magenta'
                    } else if (record.rotation === 'Yellow') {
                        return 'orange'
                    } else {
                    return 'green'
                }}) ()
                }>{text}</Tag>
        },
        {
            title: 'Break 1',
            key: 'break1',
            render: (_, record) =>
                <p>
                    <ClockCircleOutlined className={'!text-amber-500'}/> 10:20 - --:--
                </p>

        },
        {
            title: 'Lunch',
            key: 'lunch',
            render: (_, record) =>
                <p>
                    <CheckOutlined style={{color: 'green'}}/> 10:20 - 10:30
                </p>
        },
        {
            title: 'Break 2',
            key: 'break2',
            render: (_, record) =>
                <p>
                    <CloseOutlined style={{color: 'red'}}/> Not Taken
                </p>

        },
        {
            title:'',
            key: 'manage',
            width: 110,

            render: (_, record) =>
            <Button
                type={record.guard_id === selectedId ? 'primary' : 'default'}
                onClick={() => handleClick(record.guard_id)}>
                Manage
            </Button>
        }]

    return (
            <Table className={'shadow border-1 border-gray-200 rounded-t-md'} dataSource={props.data} columns={columns} pagination={false} scroll={{y: 640}} virtual rowKey="guard_id" rowHoverable={true} size={"small"}></Table>
    )
}