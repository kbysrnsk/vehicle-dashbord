"use client"
import ItemCard from '@/components/ItemCard/ItemCard'
import { Fuel } from 'lucide-react'
// import { useState } from 'react'

interface BatteryProps {
    battery:number
}

export default function Battery({battery}: BatteryProps) {
  return (
    <div>
        <ItemCard className='bg-white/80 p-2'>
            <div className='flex gap-2'>
                <Fuel />
                <p>燃料残量</p>
            </div>
            <p>{Math.floor(battery)}%</p>
        </ItemCard>
    </div>
  )
}

