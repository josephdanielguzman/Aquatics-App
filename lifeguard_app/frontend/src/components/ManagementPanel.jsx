import { Card, Form, Input } from 'antd';


export default function ManagementPanel() {
    return (
        <div className={"mt-7"}>
            <Card title={'Management Panel'}>
                <div className={'flex justify-around'}>
                    <Form>
                        <Form.Item label={'Name'}>
                            <Input />
                        </Form.Item>
                        <Form.Item label={'Name'}>
                            <Input />
                        </Form.Item>
                        <Form.Item label={'Name'}>
                            <Input />
                        </Form.Item>
                    </Form>
                    <Form>
                        <Form.Item label={'Name'}>
                            <Input />
                        </Form.Item>
                        <Form.Item label={'Name'}>
                            <Input />
                        </Form.Item>
                        <Form.Item label={'Name'}>
                            <Input />
                        </Form.Item>
                    </Form>
                </div>
            </Card>
        </div>
    )
}