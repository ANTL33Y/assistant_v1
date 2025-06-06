import { Send, Paperclip } from 'lucide-react'
import { useState } from 'react'

interface ComposerProps {
  onSend?: (text: string) => void
}

export function Composer({ onSend }: ComposerProps) {
  const [text, setText] = useState('')

  const handleSend = () => {
    if (!text.trim()) return
    onSend?.(text)
    setText('')
  }

  return (
    <div className="fixed bottom-6 left-0 right-0 lg:left-[280px] flex justify-center px-6">
      <div className="flex w-full max-w-2xl items-end bg-code-bg/50 border border-white/20 rounded-full px-4 py-2 min-h-[44px]">
        <button className="mr-2 text-muted hover:text-white">
          <Paperclip size={20} />
        </button>
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          onInput={(e) => {
            const el = e.currentTarget
            el.style.height = 'auto'
            el.style.height = el.scrollHeight + 'px'
          }}
          className="flex-1 bg-transparent resize-none focus:outline-none max-h-40 overflow-y-auto"
          rows={1}
        />
        <button onClick={handleSend} className="ml-2 text-muted hover:text-white">
          <Send size={20} />
        </button>
      </div>
    </div>
  )
}
