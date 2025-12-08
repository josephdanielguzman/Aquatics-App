import {Button} from "antd";
import {PlusOutlined} from "@ant-design/icons";
import GuardsTable from "/src/components/GuardsTable.jsx";
import ManagementPanel from "/src/components/ManagementPanel.jsx";
import {useState} from "react";
import InitializationPanel from "/src/components/InitializationPanel.jsx";
import { useGuardsOnShift} from "/src/hooks/useGuards.js";
import {Skeleton} from "antd";

export default function Dashboard() {

    const guardsOnShift = useGuardsOnShift();

    const [showInit, setInit] = useState(false);
    const [showManagement, setShowManagement] = useState(false);
    const [guardId, setSelectedGuardId] = useState(null);
    const selectedGuard = guardsOnShift.data?.find(guard => guard.guard_id === guardId);

    if (guardsOnShift.isLoading) {
        return <Skeleton active paragraph={{rows: 4}}/>
    }

    return (
        <div className={"flex flex-col gap-y-7 mt-5"}>
            <div className={'flex flex-col'}>
                <div>
                    <div className={'flex justify-end mb-2'}>
                        <Button type={showInit ? 'primary' : 'default'} onClick={() => setInit(!showInit)}
                                icon={<PlusOutlined/>}>Create</Button>
                    </div>
                    {showInit && <InitializationPanel/>}
                </div>
                <GuardsTable onGuardSelect={setShowManagement} setSelectedGuardId={setSelectedGuardId}/>
            </div>
            {showManagement && (
                <ManagementPanel setShowManagement={setShowManagement} guard={selectedGuard}/>
            )}
        </div>
    )
}