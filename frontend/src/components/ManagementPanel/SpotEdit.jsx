import {Form, Select, Button, TimePicker, Cascader} from 'antd';
import {EnvironmentOutlined} from "@ant-design/icons";
import {useGetGuardsOnShiftNoSpot, useGuardsOnShiftOnSubmit} from "/src/hooks/useGuards.js";
import {useAvailableSpots} from "/src/hooks/useRotations.js";
import {useCreateAssignment, useReplaceAssignment} from "/src/hooks/useAssignments.js";

export default function SpotEdit(props) {

    // hooks
    const guardsNoSpot = useGetGuardsOnShiftNoSpot()
    const availSpots = useAvailableSpots()
    const createAssignmentMutation = useCreateAssignment()
    const replaceAssignmentMutation = useReplaceAssignment()

    // get guard info -> swap assignments
    const guardsOnShiftMutation = useGuardsOnShiftOnSubmit({
        onSuccess: (replacementGuardInfo, variables) => {
            // create replacement assignments
            replaceAssignmentMutation.mutate({
                id: variables.old_guard,
                payload: {
                    shift_id: replacementGuardInfo[0].shift_id,
                    spot_id: variables.spot_id,
                    time: variables.time
                }
            })
        }
    })

    const hasSpot = props.guard.rotation !== null
    const rules = [{required:true}]
    const [editForm] = Form.useForm()
    const [assignForm] = Form.useForm()

    // form submission func for guard with a spot
    const handleEditSubmit = (values) => {
        guardsOnShiftMutation.mutate({
            // data to fetch replacement guard's shift id
            guardId: values.guard,
            // data to create replacement assignments
            old_guard: props.guard.guard_id,
            spot_id: props.guard.spot_id,
            time: values.time.format('HH:mm')
        })
        editForm.resetFields()
    }

    // form submission func for guard without a spot
    const handleAssignSubmit = (values) => {
        createAssignmentMutation.mutate({
            shift_id: props.guard.shift_id,
            spot_id: values.spot[1],
            time: values.time.format('HH:mm')
        })
        assignForm.resetFields()
    }

    const rotationOptions = availSpots.data?.map(r => ({
        value: r.rotation_id,
        label: r.name,
        children: r.spots.map(s => ({
            value: s.id,
            label: s.name
        })) || []
    })) || []

    const guardOptions = guardsNoSpot.data?.map(g => ({
        value: g.id,
        label: `${g.first_name} ${g.last_name}`
    })) || []

    return (
        <>
            {hasSpot ? (
                <Form
                    name={'spotEdit'}
                    layout={'vertical'}
                    form={editForm}
                    onFinish={handleEditSubmit}
                >
                    <Form.Item label={null}>
                        <p className={'text-lg'}>
                            <EnvironmentOutlined/> Remove From Spot
                        </p>
                    </Form.Item>
                    <Form.Item
                        name={'guard'}
                        rules={rules}
                        label={'Replace With:'}
                    >
                        <Select
                            options={guardOptions}
                            showSearch
                            filterOption={(input, option) =>
                                (option?.label ?? "")
                                    .toUpperCase()
                                    .includes(input.toUpperCase())
                            }
                            allowClear
                            placeholder={'Guard Name'}
                        />
                    </Form.Item>
                    <Form.Item
                        label={'Time:'}
                        name={'time'}
                        rules={[{required:true}]}
                    >
                        <TimePicker
                            className={'w-full font-normal'}
                            format={'h:mm A'}
                        />
                    </Form.Item>
                    <Form.Item
                        label={null}
                        name={'submit'}
                    >
                        <Button
                            block
                            type={'primary'}
                            htmlType={'submit'}
                        >
                            Submit
                        </Button>
                    </Form.Item>
                </Form>
                ) : (
                    <Form
                        name={'spotAssign'}
                        form={assignForm}
                        layout={'vertical'}
                        onFinish={handleAssignSubmit}
                    >
                        <Form.Item label={null}>
                            <p className={'text-lg'}>
                                <EnvironmentOutlined/> Assign Spot
                            </p>
                        </Form.Item>
                        <Form.Item
                            label={'Available Spots:'}
                            rules={rules}
                            name={'spot'}
                        >
                            <Cascader
                                options={rotationOptions}
                            />
                        </Form.Item>
                        <Form.Item
                            label={'Time:'}
                            rules={rules}
                            name={'time'}
                        >
                            <TimePicker
                            className={'w-full font-normal'}
                            format={'h:mm A'}
                            />
                        </Form.Item>
                        <Form.Item
                        label={null}
                        name={'submit'}
                        >
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