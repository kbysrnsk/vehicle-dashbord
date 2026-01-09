import React from 'react'

type ItemCardProps = {
    children: React.ReactNode
    className? : string
    onClick?: () => void
}

const ItemCard = ({children, onClick, className}: ItemCardProps) => {
  return (
    <div onClick={onClick} className={`rounded-xl ${className}`}>
        {children}
    </div>
  )
}

export default ItemCard