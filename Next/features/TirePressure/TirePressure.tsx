"use client"
import ItemCard from '@/components/ItemCard/ItemCard'
// import { useState } from 'react'
import { CircleGauge } from 'lucide-react'

interface TirePressurProps {
    tire:{
        front_right: number
        front_left: number
        rear_right: number
        rear_left: number
    }
}

export default function TirePressure({tire}: TirePressurProps) {
  return (
    <div>
        <ItemCard className='bg-white/80 p-2'>
            <div className='gap-1 flex items-center'>
                <CircleGauge />
                <p>タイヤ空気圧</p>
            </div>
            <div className='flex items-center flex-col mt-2'>
                <div className='flex gap-6'>
                    <p>{tire.front_right}kPa</p>
                    <p>{tire.front_left}kPa</p>
                </div>
                <div className='flex gap-6'>
                    <p>{tire.rear_right}kPa</p>
                    <p>{tire.rear_left}kPa</p>
                </div>

            </div>
        </ItemCard>
    </div>
  )
}

