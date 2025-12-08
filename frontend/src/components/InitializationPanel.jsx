import {AutoComplete, Button, Cascader, Form, Skeleton, TimePicker, Popconfirm} from 'antd'
import {CloseSquareFilled, UserAddOutlined} from "@ant-design/icons";
import {useCreateShift} from "/src/hooks/useShifts.js";
import {useCreateAssignment, useReplaceAssignment} from "/src/hooks/useAssignments.js";
import {useAvailableGuards, useGuardsOnShift} from "/src/hooks/useGuards.js";
import {useRotations} from "/src/hooks/useRotations.js";
import { useState } from "react";

export default function InitializationPanel() {

    // Hooks
    const availableGuards = useAvailableGuards();
    const rotations = useRotations();
    const guardsOnShift = useGuardsOnShift();
    const createShiftMutation = useCreateShift();

    const createReplacementMutation = useReplaceAssignment();
    const createShiftReplacementMutation = useCreateShift({
        onSuccess: (createdShift, variables) => {
            createReplacementMutation.mutate({
                id: variables.guard_to_replace_id,
                payload: {
                    shift_id: createdShift.id,
                    spot_id: variables.spot_id,
                    time: variables.time,
                }
            });
        }
    })

    const createAssignmentMutation = useCreateAssignment()
    const createShiftAssignmentMutation = useCreateShift({
        onSuccess: (createdShift, variables) => {
            createAssignmentMutation.mutate({
                shift_id: createdShift.id,
                spot_id: variables.spot_id,
                time: variables.started_at
            })
        }
    })

    // useStates
    const [form] = Form.useForm();
    const [open, setOpen] = useState(false);
    const [currentGuard, setCurrentGuard] = useState(null);
    const [selectedGuard, setSelectedGuard] = useState(null);
    const [formValues, setFormValues] = useState(null);

    // Placeholder if data still being fetched
    if (availableGuards.isLoading || rotations.isLoading || guardsOnShift.isLoading) {
        return <Skeleton active paragraph={{rows: 4}}/>
    }

    // Form submit
    const handleSubmit = (values) => {
        // Find guard object with a matching name
        const selectedGuard = availableGuards.data?.find(g => g.name === values.name)

        // Create shift and assignment if spot selected
        if (values.spot) {

            // Check if spot is currently occupied
            const rotation = rotations.data?.find(r => r.rotation_id === values.spot[0])
            const guardAtSpot = rotation?.spots.find(s => s.id === values.spot[1])?.current_guard

            // Display confirmation message
            if (guardAtSpot) {
                setFormValues(values)
                setSelectedGuard(selectedGuard)
                setCurrentGuard(guardAtSpot)
                setOpen(true)
            } else {
                //run mutation and assignment
                createShiftAssignmentMutation.mutate({
                    guard_id: selectedGuard.id,
                    started_at: values.started_at.format('HH:mm'),
                    spot_id: values.spot[1],
                    time: values.started_at.format('HH:mm')
                })
                form.resetFields()
            }

        // Create only shift if spot not selected
        } else {
            createShiftMutation.mutate({
                guard_id: selectedGuard.id,
                started_at: values.started_at.format('HH:mm'),
            })
            form.resetFields()
        }
    }

    const handleConfirm = () => {
        // use mutation and create assignment
        const currentGuardInfo = guardsOnShift.data?.find(g => g.name === currentGuard)

        createShiftReplacementMutation.mutate({
            // data to create shift
            guard_id: selectedGuard.id,
            started_at: formValues.started_at.format('HH:mm'),

            // data to create replacement assignments
            guard_to_replace_id: currentGuardInfo.guard_id,
            spot_id: formValues.spot[1],
            time: formValues.started_at.format('HH:mm')
        })

        setCurrentGuard(null)
        setOpen(false);
        form.resetFields();
    }

    const handleCancel = () => {
        setOpen(false);
    }

    const guards = availableGuards.data?.map(guard => ({
        value: guard.name,
        id: guard.id
    })) || []

    // Rotation and spot dropdown options
    const options = rotations.data?.map(r => ({
        value: r.rotation_id,
        label: r.name,
        children: r.spots.map(s => ({
            value: s.id,
            label: s.name
        })) || []
    })) || []

    // Filters available guards for name selection
    const filter = (inputValue, path) =>
        path.some(option => option.label.toLowerCase().includes(inputValue.toLowerCase()));

    return (
        <div className={'mb-7 bg-white rounded-md shadow h-auto font-semibold'}>
            <div className={'p-3 border-b-1 border-gray-200'}>
                <p className={'text-xl text-neutral-800'}>
                    Initialization Panel
                </p>
            </div>
            <div className={'p-4 pb-1'}>
                <Form
                    name={'guardInit'}
                    form={form}
                    layout={'vertical'}
                    onFinish={handleSubmit}
                >
                    <Form.Item
                        className={'!bg-blue-100 rounded-md !p-4'}
                        label={null}
                    >
                        <p className={'text-lg text-blue-900'}>
                            <UserAddOutlined /> Create Lifeguard:
                        </p>
                    </Form.Item>
                    <Form.Item
                        label={'Name:'}
                        name={'name'}
                        rules={[{required:true}]}
                    >
                        <AutoComplete className={'font-normal'}
                                      options={guards}
                                      filterOption={(inputValue, option) =>
                                          option?.label?.toUpperCase().indexOf(inputValue.toUpperCase()) !== -1
                        }
                                      allowClear={{ clearIcon: <CloseSquareFilled /> }}/>
                    </Form.Item>
                    <Form.Item label={'Clock-In Time:'} name={'started_at'} rules={[{required: true}]}>
                        <TimePicker className={'w-full font-normal'}
                                    format={'h:mm A'}/>
                    </Form.Item>
                    <Form.Item label={'Spot:'} name={'spot'}>
                        <Cascader className={'font-normal'}
                                  options={options}
                                  showSearch={{ filter }}/>
                    </Form.Item>
                    <Form.Item label={null}>
                        <Popconfirm className={'flex justify-center'}
                                    title={'Confirm Guard Replacement'}
                                    description={`Are you sure you want to replace ${currentGuard}?`}
                                    open={open}
                                    onConfirm={handleConfirm}
                                    onCancel={handleCancel} placement={'topLeft'}/>
                        <Form.Item label={null} name={'submit'}>
                            <Button block type={'primary'} htmlType={'submit'} >Submit</Button>
                        </Form.Item>
                    </Form.Item>
                </Form>
            </div>
        </div>
    )
}