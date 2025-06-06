// Virtualized list of chat messages
import { useEffect, useRef } from 'react'
import { useVirtualizer } from '@tanstack/react-virtual'
import { ChatMessage } from '../types'
import ChatMessageItem from './ChatMessage'

interface Props {
  messages: ChatMessage[]
}

export default function MessageList({ messages }: Props) {
  const parentRef = useRef<HTMLDivElement>(null)
  const rowVirtualizer = useVirtualizer({
    count: messages.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 60
  })

  useEffect(() => {
    rowVirtualizer.scrollToIndex(messages.length - 1)
  }, [messages.length])

  return (
    <div ref={parentRef} className="flex-1 overflow-y-auto px-4" style={{ scrollbarGutter: 'stable' }}>
      <div style={{ height: rowVirtualizer.getTotalSize() }} className="relative">
        {rowVirtualizer.getVirtualItems().map(virtualRow => {
          const message = messages[virtualRow.index]
          return (
            <div
              key={message.id}
              className="absolute top-0 left-0 w-full"
              style={{ transform: `translateY(${virtualRow.start}px)` }}
            >
              <ChatMessageItem message={message} />
            </div>
          )
        })}
      </div>
    </div>
  )
}
