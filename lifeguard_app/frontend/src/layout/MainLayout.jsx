import {Button, Layout} from 'antd';
import SideNav from '../components/SideNav.jsx';
import Date from "../components/Date.jsx";
import {PlusOutlined} from "@ant-design/icons";
import GuardsTable from "../components/GuardsTable.jsx";
import { Outlet } from "react-router-dom"

const {Sider, Content} = Layout;

export default function MainLayout() {
    return(
        <Layout>
            <Sider>
                <SideNav />
            </Sider>
            <Content className={"flex flex-col h-screen p-4 m-3"}>
                    <div className={'mb-3'}>
                        <Date />
                    </div>
                   <Outlet />
            </Content>
        </Layout>

    )
}