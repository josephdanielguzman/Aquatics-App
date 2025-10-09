import {Form} from 'antd';
import {PushpinOutlined} from "@ant-design/icons";

export default function SpotEdit() {
    return (
        <Form name={'spotEdit'}>
            <Form.Item label={null}>
                <p className={'text-lg'}><PushpinOutlined/> Modify Spot</p>
            </Form.Item>
        </Form>
    )
}