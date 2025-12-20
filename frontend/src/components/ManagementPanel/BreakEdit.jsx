import {Button, Form, message, TimePicker} from 'antd';
import {ClockCircleOutlined, HomeOutlined} from "@ant-design/icons";
import {useCreateBreak, useUpdateBreak} from "/src/hooks/useBreaks.js";
import {useUpdateShift} from "/src/hooks/useShifts.js";
import dayjs from 'dayjs'

export default function BreakEdit(props) {

    // hooks
    const createBreakMutation = useCreateBreak()
    const updateBreakMutation = useUpdateBreak()
    const updateShiftMutation = useUpdateShift({
        onSuccess: () => {
            props.setSelectedGuardId(null)
            props.setShowManagement(false)
        }
    })

    // useStates
    const [form] = Form.useForm()
    const [messageApi, contextHolder] = message.useMessage()

    const format ='h:mm A'
    const breakTypes = ['Break 1', 'Lunch', 'Break 2']
    const openBreak = props.guard.breaks?.find(b => b.ended === null)
    let nextBreak = null
    let startTime = null

    // Find next break type
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
            // Validate break isn't < 10 mins
            if (openBreak.type !== 2) {
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
            } else {
                // Validate lunch isn't < 30 mins
                if (values.time.diff(startTime, 'minute') < 30) {
                    messageApi.open({
                        type: 'error',
                        content: 'Lunch less than 30 minutes',
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
    }

    const handleClockOut = (values) => {
        updateShiftMutation.mutate({
            shift_id: props.guard.shift_id,
            payload: {
                ended_at: values.time.format('HH:mm')
            }
        })
    }

    return (
        <>
            {contextHolder}
            {props.breakAvailable ? (
                <Form
                    name={'breakEdit'}
                    layout={'vertical'}
                    form={form}
                    onFinish={handleSubmit}
                >
                    <Form.Item label={null}>
                        <p className={'text-lg'}>
                            <ClockCircleOutlined/>
                            {openBreak ? ` Finish ${breakTypes[openBreak.type - 1]}`
                                       : ` Send on ${breakTypes[nextBreak - 1]}`}
                        </p>
                    </Form.Item>
                    <Form.Item
                        label={'Time:'}
                        name={'time'}
                        rules={[{required:true}]}
                    >
                        <TimePicker
                            className='w-full font-normal'
                            format={format}
                        />
                    </Form.Item>
                    <Form.Item
                        label={null}
                        name={'submit'}
                    >
                        <Button
                            type={'primary'}
                            block htmlType={'submit'}
                        >
                            Submit
                        </Button>
                    </Form.Item>
                </Form>
            ) : (
                <Form
                    name={'clockOut'}
                    onFinish={handleClockOut}
                    layout={'vertical'}
                >
                    <Form.Item label={null}>
                        <p className={'text-lg'}>
                            <HomeOutlined/> Send Home
                        </p>
                    </Form.Item>
                    <Form.Item
                        name={'time'}
                        label={'Time'}
                        rules={[{required: true}]}
                    >
                        <TimePicker
                            className='w-full font-normal'
                            format={format}
                        />
                    </Form.Item>
                    <Form.Item>
                        <Button
                            block
                            type={'primary'}
                            htmlType={'submit'}
                        >
                            Submit
                        </Button>
                    </Form.Item>
                </Form>
            )}

        </>
    )
}