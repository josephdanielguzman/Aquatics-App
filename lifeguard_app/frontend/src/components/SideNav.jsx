import tailwindcss from 'tailwindcss'
import { Menu } from "antd";
import {NavLink} from "react-router-dom";
import {HomeOutlined, ReloadOutlined, AuditOutlined} from '@ant-design/icons'

export default function Sidebar() {
    return (
        <Menu defaultSelectedKeys={'1'} theme='dark' className={"text-center"}>
            <div className={'bg-black h-25 w-25'}>
                <p className={"pt-10"}>placeholder</p>
            </div>
            <Menu.Item key={'1'} icon={<HomeOutlined />}><NavLink to={'/'}>Home</NavLink></Menu.Item>
            <Menu.Item key={'2'} icon={<ReloadOutlined />}><NavLink to={'/Rotations'}>Rotations</NavLink></Menu.Item>
            <Menu.Item key={'3'} icon={<AuditOutlined />}><NavLink to={'/Reports'}>Reports</NavLink></Menu.Item>
        </Menu>
    )
}
