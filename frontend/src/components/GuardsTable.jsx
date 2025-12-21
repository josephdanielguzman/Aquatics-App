import { Table, Button, Tag, Input, Space } from 'antd';
import {
    CheckOutlined,
    ClockCircleOutlined,
    CloseOutlined,
    SearchOutlined
} from "@ant-design/icons";
import {useState, useRef} from "react";
import {useGuardsOnShift} from "/src/hooks/useGuards.js";
import { formatTime } from "/src/utils/formatTime.js";

export default function GuardsTable(props){

    // hooks
    const guardsOnShift = useGuardsOnShift()

    // useStates
    const [selectedId, setSelectedId] = useState(null);
    const [searchText, setSearchText] = useState('')
    const [searchedColumn, setSearchedColumn] = useState('')

    const searchInput = useRef(null);

    const findBreak = (record, breakType) => {
        const b = record.breaks?.find(b => b.type === breakType);

        if(!b) {
            return (<p><CloseOutlined className={'!text-red-500'}/> Not Taken</p>)
        } else {
            if(b.ended) {
                return (<p><CheckOutlined className={'!text-green-700'}/> {formatTime(b.started)} - {formatTime(b.ended)}</p>)
            } else {
                return (<p><ClockCircleOutlined className={'!text-amber-500'}/> {formatTime(b.started)} - --:--</p>)
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
    const handleSearch = (selectedKeys, confirm, dataIndex) => {
        confirm();
        setSearchText(selectedKeys[0]);
        setSearchedColumn(dataIndex);
    }

    const getColumnSearchProps = dataIndex => ({
        filterDropdown: ({ setSelectedKeys, selectedKeys, confirm, clearFilters, close }) => (
          <div style={{ padding: 8 }} onKeyDown={e => e.stopPropagation()}>
            <Input
              ref={searchInput}
              placeholder={`Search ${dataIndex}`}
              value={selectedKeys[0]}
              onChange={e => setSelectedKeys(e.target.value ? [e.target.value] : [])}
              onPressEnter={() => handleSearch(selectedKeys, confirm, dataIndex)}
              style={{ marginBottom: 8, display: 'block' }}
            />
            <Space>
              <Button
                type="primary"
                onClick={() => {
                    handleSearch(selectedKeys, confirm, dataIndex)
                    confirm({ closeDropdown: true })
                }}
                icon={<SearchOutlined />}
                size="small"
                style={{ width: 90 }}
              >
                Search
              </Button>
              <Button
                onClick={() => {
                    clearFilters && handleReset(clearFilters)
                    handleSearch(selectedKeys, confirm, dataIndex)
                }}
                size="small"
                style={{ width: 60 }}
              >
                Reset
              </Button>
              <Button
                type="link"
                size="small"
                onClick={() => {
                  close();
                }}
              >
                close
              </Button>
            </Space>
          </div>
        ),
        filterIcon: filtered => <SearchOutlined style={{ color: filtered ? '#1677ff' : undefined }} />,
        onFilter: (value, record) =>
          record[dataIndex].toString().toLowerCase().includes(value.toLowerCase()),
        filterDropdownProps: {
          onOpenChange(open) {
            if (open) {
              setTimeout(() => searchInput.current?.select(), 100);
            }
          },
        },
        render: text =>
          searchedColumn === dataIndex ? (
            text.toString()
          ) : (
            text
          ),
    })

    const handleReset = clearFilters => {
        clearFilters()
        setSearchText('')
    }

    const columns = [
        {
            title: 'Name',
            dataIndex: 'name',
            key: 'name',
            ...getColumnSearchProps('name')
        },
        {
            title: 'Clock-In',
            dataIndex: 'clock_in',
            key: 'clock_in',
            width: 150,
            render: (text, record) =>
                (<p>{formatTime(text)}</p>)
            ,
            // chronologically sort times
            sorter: (a, b) => a.clock_in.localeCompare(b.clock_in),
            defaultSortOrder: 'ascend',
            sortDirections: ['ascend', 'descend']
        },
        {
            title: 'Spot',
            dataIndex: 'spot_name',
            key: 'spot_name',
            render: (text, record) => {

                if (!text) {
                    return <p>N/A</p>
                } else {
                    return (<Tag style={{fontSize: '14px'}}
                                          color={(() => {
                                            if (record.rotation === 'Violet') {
                                                return 'magenta'
                                            } else if (record.rotation === 'Yellow') {
                                                return 'orange'
                                            } else if (record.rotation === 'Green'){
                                                return 'green'
                                            }
                                          }) ()}>{text}
                    </Tag>)
                }
            }
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
            <Table
                className={'shadow border-1 border-gray-200 rounded-t-md'}
                dataSource={guardsOnShift.data}
                columns={columns}
                pagination={false}
                scroll={{y: 640}}
                virtual
                rowKey="guard_id"
                rowHoverable={true}
                size={"small"}></Table>
    )
}