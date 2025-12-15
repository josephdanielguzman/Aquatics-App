import {Button, Form, message, TimePicker} from 'antd';
import {ClockCircleOutlined} from "@ant-design/icons";
import {useCreateBreak, useUpdateBreak} from "/src/hooks/useBreaks.js";
import dayjs from 'dayjs'

export default function BreakEdit(props) {
    const format ='h:mm A'

    const createBreakMutation = useCreateBreak()
    const updateBreakMutation = useUpdateBreak()
    const [form] = Form.useForm()
    const [messageApi, contextHolder] = message.useMessage()

    const breakTypes = ['Break 1', 'Lunch', 'Break 2']
    const openBreak = props.guard.breaks?.find(b => b.ended === null)
    let nextBreak = null
    let startTime = null

    if (!openBreak) {
        if (props.guard.breaks.length === 0)
        {
            nextBreak = 1
        } else if (props.guard.breaks.length === 1) {
            nextBreak = 2
        } else {
            nextBreak = 3
        }
    } else {
        startTime = dayjs(openBreak.started, 'HH:mm:ss')
    }

    const handleSubmit = (values) => {
        if (!openBreak) {
            createBreakMutation.mutate({
                shift_id: props.guard.shift_id,
                type: nextBreak,
                start_time: values.time.format('HH:mm')

            })
        } else {
            if (values.time.diff(startTime, 'minute') < 10) {
                messageApi.open({
                    type: 'error',
                    content: 'Break less than 10 minutes',
                })
            } else {
                updateBreakMutation.mutate({
                    id: openBreak.id,
                    payload: {
                        end_time: values.time.format('HH:mm')
                    }
                })
            }
        }
    }

    return (
        <>
            {contextHolder}
            <Form name={'breakEdit'} layout={'vertical'} form={form} onFinish={handleSubmit}>
                <Form.Item label={null}>
                    <p className={'text-lg'}>
                        <ClockCircleOutlined/>
                        {openBreak ? ` Finish ${breakTypes[openBreak.type - 1]}`
                                   : ` Send on ${breakTypes[nextBreak - 1]}`}
                    </p>
                </Form.Item>
                <Form.Item label={'Time:'} name={'time'} rules={[{required:true}]}>
                    <TimePicker className='w-full font-normal' format={format}></TimePicker>
                </Form.Item>
                <Form.Item label={null} name={'submit'}>
                    <Button type={'primary'} block htmlType={'submit'}>Submit</Button>
                </Form.Item>
            </Form>
        </>
    )
}