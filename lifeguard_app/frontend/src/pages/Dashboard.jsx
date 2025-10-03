import Date from "../components/Date.jsx";
import {Button} from "antd";
import {PlusOutlined} from "@ant-design/icons";
import GuardsTable from "../components/GuardsTable.jsx";
import { Content } from "antd/es/layout/layout.js";
import ManagementPanel from "../components/ManagementPanel.jsx";

export default function Dashboard() {
    return (
        <Content className={"flex flex-col h-screen mt-2"}>
            <div className={"flex justify-end mb-2"}>
                <Button icon={<PlusOutlined/>}>Create</Button>
            </div>
            <GuardsTable/>
            <div>
                <ManagementPanel />
            </div>
        </Content>
    )
}