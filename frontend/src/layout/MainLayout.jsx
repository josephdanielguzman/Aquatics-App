import { Layout} from 'antd';
import SideNav from '../components/SideNav.jsx';
import HeaderDate from "../components/HeaderDate.jsx";
import { Outlet } from "react-router-dom"

const {Sider, Content} = Layout;

export default function MainLayout() {
    return(
        <Layout className={'h-screen'}>
            <Sider>
                <SideNav />
            </Sider>
            <Content className={"flex flex-col p-4 overflow-y-auto"}>
                <HeaderDate />
                <Outlet />
            </Content>
        </Layout>
    )
}