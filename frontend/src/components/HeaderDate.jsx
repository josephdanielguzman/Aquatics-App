import { useState, useEffect } from 'react'

export default function HeaderDate() {

    const[time, setTime] = useState(new Date())

    useEffect(() => {
        setInterval(() => setTime(new Date()), 1000)
    },[])

    return (
        <div className={"flex justify-between font-sans font-semibold text-blue-950"}>
            <div >
                <p className={"text-2xl"}>{time.toLocaleDateString('en-US', {weekday: 'long'})}</p>
                <p className={'font-normal'}>{time.toLocaleDateString('en-US', {month: 'long', day: 'numeric', year: 'numeric'})}</p>
            </div>
            <div className={"text-2xl"}>
                {time.toLocaleTimeString('en-US', {hour: '2-digit', minute: '2-digit'})}
            </div>
        </div>
    )
}