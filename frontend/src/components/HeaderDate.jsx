
export default function HeaderDate() {
    const time = new Date().toLocaleTimeString([], {hour: '2-digit', minute: '2-digit', hour12: true});
    return (
        <div className={"flex justify-between font-sans font-semibold text-blue-950"}>
            <div >
                <p className={"text-2xl"}>Monday</p>
                <p className={'font-normal'}>September 2, 2025</p>
            </div>
            <div className={"text-2xl"}>
                {time}
            </div>
        </div>
    )
}