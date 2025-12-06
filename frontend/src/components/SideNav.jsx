import { Menu } from "antd";
import {NavLink} from "react-router-dom";
import {HomeOutlined, ReloadOutlined, AuditOutlined} from '@ant-design/icons'

export default function Sidebar() {
    return (
        <Menu defaultSelectedKeys={'1'} theme='dark' className={"text-center"}>
            <div className={'flex gap-x-2 mt-2 mb-3 h-12 text-left pl-4 pt-2 text-2xl font-semibold'}>
                <img src={"/src/assets/blue-buoy.png"} className={"pt-2"}/><p className={"flex flex-col justify-end"}>GuardSync</p>
            </div>
            <Menu.Item key={'1'} icon={<HomeOutlined />}><NavLink to={'/'}>Home</NavLink></Menu.Item>
            <Menu.Item key={'2'} icon={<ReloadOutlined />}><NavLink to={'/Rotations'}>Rotations</NavLink></Menu.Item>
            <Menu.Item key={'3'} icon={<AuditOutlined />}><NavLink to={'/Reports'}>Reports</NavLink></Menu.Item>
        </Menu>
    )
}
