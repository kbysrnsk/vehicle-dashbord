"use client"
import ItemCard from '@/components/ItemCard/ItemCard'
import { Thermometer } from 'lucide-react'
import { useState } from 'react'
import { TempControl } from './TempControl'

interface AirConditionProps {
    temperature:{
        in: number
        out: number
    },
    target_temp:number
}

export default function AirCondition({temperature, target_temp}: AirConditionProps) {
    const [open, setOpen] = useState(false)
  return (
    <div>
        <ItemCard onClick={() => setOpen(true)} className='bg-white/80 p-2'>
            <div className='gap-1 flex items-center'>
                <Thermometer/>
                <p>温度</p>
            </div>
            <div className='flex gap-6 justify-center'>
                <div className='grid gap-1 mt-1'>
                    <p>車内：{temperature.in}℃</p>
                    <p>車外：{temperature.out}℃</p>
                </div>
            </div>
        </ItemCard>

        {open && (
            <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-2">
                <div className="bg-white p-4 rounded">
                    <p>温度</p>
                    <div className='flex gap-6 justify-center'>
                    <div className='grid gap-1 mt-1'>
                            <p>車内：{temperature.in}℃</p>
                            <p>車外：{temperature.out}℃</p>
                        </div>
                    </div>
                    <TempControl 
                    initial={target_temp}
                    onChange={async (value) => { 
                        try { 
                            const res = await fetch("/api/updateTarget", { 
                                method: "POST", 
                                headers: { "Content-Type": "application/json", }, 
                                body: JSON.stringify({ vehicle_id: process.env.NEXT_PUBLIC_TEST_VEHICLE_ID, target_temp: value, }), 
                            }); 
                            if (!res.ok) { 
                                console.error("API error:", await res.text()); 
                            } 
                        } catch (err) { 
                            console.error("Network error:", err); 
                        } 
                    }}
                    />
                    <button onClick={() => setOpen(false)}>閉じる</button>
                </div>
            </div>
        )}
    </div>
  )
}

