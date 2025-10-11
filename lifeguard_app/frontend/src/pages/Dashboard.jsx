import Date from "../components/HeaderDate.jsx";
import {Button} from "antd";
import {PlusOutlined} from "@ant-design/icons";
import GuardsTable from "../components/GuardsTable.jsx";
import { Content } from "antd/es/layout/layout.js";
import ManagementPanel from "../components/ManagementPanel.jsx";
import {useState} from "react";
import {useQuery} from "@tanstack/react-query";


export default function Dashboard() {

    const {data} = useQuery({
        queryKey: ['guards'],
        queryFn: getGuards
    })

    const [showManagement, setShowManagement] = useState(false);
    const [guardId, setSelectedGuardId] = useState(null);
    const selectedGuard = data?.find(guard => guard.guard_id === guardId);

    return (
        <div className={"flex flex-col gap-y-7 mt-5"}>
            <div>
                <div className={"flex justify-end mb-1"}>
                    <Button icon={<PlusOutlined/>}>Create</Button>
                </div>
                <GuardsTable data={data} onGuardSelect={setShowManagement} setSelectedGuardId={setSelectedGuardId} />
            </div>
            {showManagement && (
                <div>
                <ManagementPanel guard={selectedGuard}/>
                </div>
            )}
        </div>
    )
}

const getGuards = async () => {
    const response = await fetch('http://127.0.0.1:8000/guards/status')
    return response.json()
}