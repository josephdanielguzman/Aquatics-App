import { Table, Button, Tag } from 'antd';
import {useQuery} from "@tanstack/react-query";


export default function GuardsTable(){

    const {data} = useQuery({
        queryKey: ['guards'],
        queryFn: getGuards
    })

    const columns = [
        {
            title: 'Name',
            dataIndex: 'first_name',
            key: 'first_name',
            width: 350
        },
        {
            title: 'Spot',
            key: 'spot',
            width: 300,
            render: (_, record) =>
                <Tag color={'green'}>Top of Red and Blue</Tag>
        },
        {
            title: 'Break 1',
            key: 'break1',
        },
        {
            title: 'Lunch',
            key: 'lunch',
        },
        {
            title: 'Break 2',
            key: 'break2',
            render: (_, record) =>
                <Tag color="red">Not Taken</Tag>
        },
        {
            title:'Action',
            key: 'action',
            width: 100,

            //TODO: Make row blue on selection
            render: (_, record) =>
            <Button type={"default"}>Select</Button>
        }]

    return (
        <div>
            <Table  dataSource={data} columns={columns} pagination={false} scroll={{y: 640}} virtual rowKey='id' rowHoverable={true} size={"middle"}></Table>
        </div>
    )
}

const getGuards = async () => {
    const response = await fetch('http://127.0.0.1:8000/guards')
    return response.json()
}