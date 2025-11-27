import tailwindcss from 'tailwindcss'
import { Menu } from "antd";
import {NavLink} from "react-router-dom";
import {HomeOutlined, ReloadOutlined, AuditOutlined} from '@ant-design/icons'

export default function Sidebar() {
    return (
        <Menu defaultSelectedKeys={'1'} theme='dark' className={"text-center"}>
            <div className={'flex flex-col justify-items-center h-20 mt-2 text-left pl-3 text-2xl font-semibold'}>
                <p>Shift</p>
                <p>Manager</p>
            </div>
            <Menu.Item key={'1'} icon={<HomeOutlined />}><NavLink to={'/'}>Home</NavLink></Menu.Item>
            <Menu.Item key={'2'} icon={<ReloadOutlined />}><NavLink to={'/Rotations'}>Rotations</NavLink></Menu.Item>
            <Menu.Item key={'3'} icon={<AuditOutlined />}><NavLink to={'/Reports'}>Reports</NavLink></Menu.Item>
        </Menu>
    )
}
