import {Button, Form, Select, TimePicker} from 'antd';
import {ClockCircleOutlined} from "@ant-design/icons";

export default function BreakEdit() {
    const format ='h:mm A'
    return (
        <Form name={'breakEdit'} layout={'vertical'}>
            <Form.Item label={null}>
                <p className={'text-lg'}><ClockCircleOutlined/> Send on Break/Lunch</p>
            </Form.Item>
            <Form.Item label={'Break/Lunch Type:'} name='breakType' rules={[{required:true}]}>
                <Select>
                    <Select.Option value={'break1'}>Break 1</Select.Option>
                    <Select.Option value={'lunch'}>Lunch</Select.Option>
                    <Select.Option value={'break2'}>Break 2</Select.Option>
                </Select>
            </Form.Item>
            <Form.Item label={'Time:'} name={'breakTime'} rules={[{required:true}]}>
                <TimePicker className='w-full' format={format}></TimePicker>
            </Form.Item>
            <Form.Item label={'Replace With:'}>
            </Form.Item>
            <Form.Item label={null}>
                <Button type={'primary'} block>Submit</Button>
            </Form.Item>
        </Form>
    )
}