import { useQuery } from '@tanstack/react-query'
import { Table } from 'antd'

export default function GuardsTable() {

    const {data} = useQuery({
        queryKey: ['guards'],
        queryFn: getGuards
    });

    const columns = [
        {
            title: 'ID',
            dataIndex: 'id',
            key: 'id',
        },
        {
            title: "First Name",
            dataIndex: 'first_name',
            key: 'first_name',
        },
        {
            title: "Last Name",
            dataIndex: 'last_name',
            key: 'last_name',
        },
    ];

    return (
        <Table dataSource={data} columns={columns} rowKey="id"></Table>
    )
}

const getGuards = async () => {
    const response = await fetch("http://127.0.0.1:8000/guards")
    return response.json()
}