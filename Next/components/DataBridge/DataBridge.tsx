"use client"
import AirCondition from "@/features/AirCondition/AirCondition";
import Battery from "@/features/Battery/Battery";
import DoorLock from "@/features/Lock/DoorLock";
import Mileage from "@/features/Mileage/Mileage";
import Speed from "@/features/Speed/Speed";
import TirePressure from "@/features/TirePressure/TirePressure";
import { useEffect, useState } from "react";
import Image from 'next/image';
import OnlineStatus from "@/features/OnlineStatus/OnlineStatus";
import Map from "@/features/Map/Map";


const DataBridge = ({initialdata}) => {
    const [data, setData] = useState(initialdata)
    const safe = (value) => { return value === undefined || value === null ? "-" : value; };
    useEffect(() => {
        const updateData = async () => { 
            const baseUrl = process.env.NEXT_PUBLIC_BASE_URL
            const newdata = await fetch(`${baseUrl}/api/getdata`, {cache: "no-store"}).then((res) => res.json());
            setData(newdata) 
        }
        const interval = setInterval(updateData, 1000)
        return () => clearInterval(interval)
    },[])

    const IG = data.state?.payload?.IG; 
    const disconnect = data.state?.payload?.disconnect; 
    const isEngineStopped = IG === false; 
    const isDisconnected = disconnect === true; 
    const disableAll = isEngineStopped || isDisconnected;
    const running_status = data.state.payload.status;

  return (
    <div className="bg-zinc-900 min-h-full pb-10">
        {disableAll && (
            <div className="fixed inset-0 bg-black/60 z-[9999] flex items-center justify-center text-white text-2xl">
            {isDisconnected ? "通信が切断されました" : "車は安全に停止しています"}
            </div>
        )}
        <section className="h-[50vh] flex justify-center items-center relative">
            <div className="absolute top-6 right-6 z-1">
                <DoorLock is_locked = {safe(data.state?.payload?.door_locked)} disabled = {running_status}/>
            </div>
            <div className="z-1">
                <OnlineStatus online_status={safe(data.state?.payload?.online)}/>
            </div>
            <div className="h-[50vh] w-full relative absolute">
                <Image src="/vehicle_sample.png" alt="" fill sizes = "80vw" style ={{objectFit: "contain"}} />
            </div>
        </section>
        <div className="w-screen grid grid-cols-2 gap-2 p-2 mb-4">
            <Battery battery = {safe(data.state?.payload?.battery)}/>
            <Speed speed = {safe(data.state?.payload?.speed)}/>
            <AirCondition  temperature = {safe(data.state?.payload?.temperature)} target_temp={safe(data.target?.target?.target_temp)}/>
            <TirePressure tire = {safe(data.state?.payload?.tire_pressure)}/>
            <Mileage mileage = {safe(data.state?.payload?.mileage)}/>
        </div>
        <p className="text-white w-full pl-6 ">現在位置</p>
        <section className="h-[50vh] m-4 border border-black text-center rounded-xl overflow-hidden flex justify-center items-center z-0">
            <Map position={data.state?.payload?.position ?? null}/>
        </section>
    </div>
  )
}

export default DataBridge