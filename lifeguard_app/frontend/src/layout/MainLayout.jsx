import {Button, Layout} from 'antd';
import SideNav from '../components/SideNav.jsx';
import Date from "../components/Date.jsx";
import {PlusOutlined} from "@ant-design/icons";
import GuardsTable from "../components/GuardsTable.jsx";
import { Outlet } from "react-router-dom"

const {Sider, Content} = Layout;

export default function MainLayout() {
    return(
        <Layout className={'h-screen'}>
                <Sider>
                    <SideNav />
                </Sider>
            <Content className={"flex flex-col p-4 overflow-y-auto"}>
                <Date />
                <Outlet />
            </Content>
        </Layout>
    )
}