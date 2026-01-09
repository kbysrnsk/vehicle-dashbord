"use client"
import ItemCard from '@/components/ItemCard/ItemCard'
import { useState } from 'react'


export default function Hazard() {
    const [open, setOpen] = useState(false)
  return (
    <div>
        <ItemCard onClick={() => setOpen(true)}>
            <p>Hazard</p>
        </ItemCard>

        {open && (
            <div className="fixed inset-0 bg-black/50 flex items-center justify-center">
                <div className="bg-white p-4 rounded">
                    <p>モーダルの内容</p>
                    <button onClick={() => setOpen(false)}>閉じる</button>
                </div>
            </div>
        )}
    </div>
  )
}

