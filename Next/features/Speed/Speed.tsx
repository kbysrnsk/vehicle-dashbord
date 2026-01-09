"use client"
import ItemCard from '@/components/ItemCard/ItemCard'
import { Gauge } from 'lucide-react'
// import { useState } from 'react'

interface SpeedProps {
    speed:number
}

export default function Speed({speed}: SpeedProps) {
  return (
    <div>
        <ItemCard className='bg-white/80 p-2'>
            <div className='gap-1 flex items-center'>
                <Gauge />
                <p>速度</p>
            </div>
            <p>{Math.floor(speed)}km/h</p>
        </ItemCard>
    </div>
  )
}

