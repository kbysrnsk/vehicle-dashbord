interface OnlineProps {
    online_status:boolean
}

export default function OnlineStatus({online_status}: OnlineProps) {
    const online = online_status
  return (
    <div className="absolute top-8 left-6 text-white z-50 flex items-center gap-2 ">
        <span
            className={`
            w-3 h-3 rounded-full 
            ${online ? "bg-lime-300 shadow-[0_0_10px_4px_#bef264]" 
                    : "bg-red-500 shadow-[0_0_8px_#ef4444]"}
            `}
        />
        <span>{online? "オンライン" : "オフライン"}</span>
        {/* <div className="fixed inset-0 bg-black/70 backdrop-blur-sm z-10 flex items-center justify-center h-[100vh] w-[100vw]"></div> */}
    </div>
  )
}

