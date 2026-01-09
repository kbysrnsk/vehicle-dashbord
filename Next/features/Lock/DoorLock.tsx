"use client"
import ItemCard from '@/components/ItemCard/ItemCard'
import { useState } from 'react'
import { Lock, LockOpen } from 'lucide-react'

interface DoorLockProps {
  is_locked : boolean
  disabled : number
}

export default function DoorLock({is_locked, disabled}: DoorLockProps) {
  const [open, setOpen] = useState(false)
  const lock = is_locked
  const isDisabled = disabled === 1

  const handleConfirm = async () => {
    const newLockState = !lock
    setOpen(false)

    try { 
      await fetch("/api/updateLock", { 
        method: "POST", 
        headers: { "Content-Type": "application/json" }, 
        body: JSON.stringify({door_locked: newLockState ? 1 : 0 }) 
      }) 
    } catch (err) { 
      console.error("Lock API error:", err) 
    }
  }

  return (
    <div>
      <ItemCard onClick={() => setOpen(true)} className={`p-2 ${lock ? "bg-red-500" : "bg-green-500"} ${isDisabled? "bg-gray-500 text-gray-300 cursor-not-allowed opacity-60 pointer-events-none": ""}`}>
        <div className='gap-1 flex items-center'>
          {lock ? <Lock className="text-white"/> : <LockOpen className="text-white"/>}
          <span className='text-white'>Door</span>
        </div>
      </ItemCard>

      {open && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center ">
          <div className="bg-white p-4 rounded space-y-4">
            <p>{lock ? "ロックを解除しますか？" : "ロックしますか？"}</p>

            <div className="flex gap-2 justify-end">
              <button className="px-3 py-1 bg-gray-200 rounded" onClick={() => setOpen(false)}>
                <span>キャンセル</span>
              </button>

              <button className={`px-3 py-1 bg-blue-500 text-white rounded ${isDisabled? "bg-gray-500 text-gray-300 cursor-not-allowed opacity-60 pointer-events-none": ""}`} onClick={handleConfirm} >
                <span>OK</span>
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
