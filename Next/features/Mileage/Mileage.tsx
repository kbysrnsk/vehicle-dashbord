"use client"
import ItemCard from '@/components/ItemCard/ItemCard'
// import { useState } from 'react'

interface MileageProps {
    mileage: number
}

export default function Mileage({mileage}:MileageProps) {
  return (
    <div>
        <ItemCard className='bg-white/80 p-2'>
            <p>総走行距離</p>
            <p>{mileage}km</p>
        </ItemCard>
    </div>
  )
}

