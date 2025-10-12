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

    const findBreak = (record, breakType) => {
        const b = record.breaks?.find(b => b.type === breakType);

        if(!b) {
            return (<p><CloseOutlined className={'!text-red-500'}/> Not Taken</p>)
        } else {
            if(b.ended) {
                return (<p><CheckOutlined className={'!text-green-700'}/> {b.started} - {b.ended}</p>)
            } else {
                return (<p><ClockCircleOutlined className={'!text-amber-500'}/> {b.started} - --:--</p>)
            }
        }
    }

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
            render: (_, record) => findBreak(record, 1)
        },
        {
            title: 'Lunch',
            key: 'lunch',
            render: (_, record) => findBreak(record, 2)
        },
        {
            title: 'Break 2',
            key: 'break2',
            render: (_, record) => findBreak(record, 3)
        },
        {
            title:'',
            key: 'manage',
            width: 110,
            className: 'button-column',

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