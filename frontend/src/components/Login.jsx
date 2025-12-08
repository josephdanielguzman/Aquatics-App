import { useLogin } from '../hooks/useAuth.js'
import {Button, Form, Input} from 'antd'

export default function Login() {

    const loginMutation = useLogin()
    const [form] = Form.useForm()

    const handleSubmit = (values) => {
        loginMutation.mutate({
            username: values.username,
            password: values.password
        })

        //todo: reset form fields
        form.resetFields()
    }

    return (
        <div className={"flex justify-center items-center w-screen h-screen bg-gray-100"}>
            <div className={"flex flex-col bg-slate-900 w-120 h-140 rounded-4xl p-10 gap-y-15 shadow-2xl"}>
                <div className={"flex justify-center gap-x-3"}>
                    <img
                        src={"/src/assets/blue-buoy.png"}
                        alt="lifeguard buoy"
                        className={"pt-2 h-12"}
                    />
                    <p className={"flex flex-col justify-end font-bold text-4xl text-gray-400"}>
                        GuardSync
                    </p>
                </div>
                <Form
                    name={"auth"}
                    layout={"vertical"}
                    onFinish={handleSubmit}
                >
                    <Form.Item
                        label={<span className={"form-text"}>Username</span>}
                        name={"username"}
                        rules={[{required: true, message: "Username is required."}]}
                        layout={"vertical"}
                        className={"font-semibold"}
                    >
                        <Input />
                    </Form.Item>
                    <Form.Item
                        label={<span className={"form-text"}>Password</span>}
                        name={"password"}
                        rules={[{required: true, message: "Password is required."}]}
                        layout={"vertical"}
                        className={"font-semibold !mt-15"}
                    >
                        <Input />
                    </Form.Item>
                    <Form.Item
                        label={null}
                        name={'submit'}
                    >
                            <Button
                                block type={'primary'}
                                htmlType={'submit'}
                                className={"!bg-blue-700 mt-20 !h-10 !font-semibold !text-lg"}
                            >
                                Login
                            </Button>
                    </Form.Item>
                </Form>
            </div>
        </div>
    )
}