import Date from "../components/Date.jsx";
import {Button} from "antd";
import {PlusOutlined} from "@ant-design/icons";
import GuardsTable from "../components/GuardsTable.jsx";
import { Content } from "antd/es/layout/layout.js";
import ManagementPanel from "../components/ManagementPanel.jsx";

export default function Dashboard() {
    return (
        <div className={"flex flex-col gap-y-7 mt-5"}>
            <div>
                <div className={"flex justify-end mb-1"}>
                    <Button icon={<PlusOutlined/>}>Create</Button>
                </div>
                <GuardsTable/>
            </div>
            <div>
                <ManagementPanel />
            </div>
        </div>
    )
}